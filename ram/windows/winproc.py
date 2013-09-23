# Copyright (C) 2009-2013 ArxSys
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
#
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
#
# Author(s):
#  Frederic Baguelin <fba@digital-forensic.org>
#

import traceback

from dff.api.vfs.libvfs import Node, FileMapping
from dff.api.vfs.vfs import vfs
from dff.api.types.libtypes import VMap, Variant, VList, vtime, TIME_MS_64, typeId

import volatility.obj as obj


import sys
sys.path.append("/home/udgover/sources/pefile-1.2.10-123")

try:
    import pefile
    PEFILE_FOUND = True
except:
    PEFILE_FOUND = False


def confswitch(func):
    def switch(self, *args):
        self._fsobj._config.switchContext()
        return func(self, *args)
    return switch


class WinMapper():
    def __init__(self):
        self._aspace = None
        self._baseaddr = -1
        self._fsobj = None

        
    def _fileMapping(self, fm):
        if self._aspace is None or self._baseaddr == -1 or self._fsobj is None:
            return
        try:
            dos_header = obj.Object("_IMAGE_DOS_HEADER", 
                                    offset = self._baseaddr,
                                    vm = self._aspace)
            nt_header = dos_header.get_nt_header()
            soh = nt_header.OptionalHeader.SizeOfHeaders
            header_off = self._aspace.vtop(self._baseaddr)
            real_size = len(self._aspace.zread(self._baseaddr, soh))
            fm.push(0, real_size, self._fsobj.memdump, long(header_off))
            fa = nt_header.OptionalHeader.FileAlignment
            for sect in nt_header.get_sections(True):
                foa = self.__round(sect.PointerToRawData, fa)
                data_start = long(sect.VirtualAddress + self._baseaddr)
                data_size = long(sect.SizeOfRawData)
                offset = long(foa)
                first_block = 0x1000 - data_start % 0x1000
                full_blocks = ((data_size + (data_start % 0x1000)) / 0x1000) - 1
                left_over = (data_size + data_start) % 0x1000
                paddr = self._aspace.vtop(data_start)
                if data_size < first_block:
                    real_size = len(self._aspace.zread(data_start, data_size))
                    self.__push(fm, offset, real_size, paddr)
                else:
                    real_size = len(self._aspace.zread(data_start, first_block))
                    self.__push(fm, offset, real_size, paddr)
                    offset += real_size
                    new_vaddr = data_start + first_block
                    for _i in range(0, full_blocks):
                        paddr = self._aspace.vtop(new_vaddr)
                        real_size = len(self._aspace.zread(new_vaddr, 0x1000))
                        self.__push(fm, offset, real_size, paddr)
                        new_vaddr = new_vaddr + 0x1000
                        offset += real_size
                    if left_over > 0:
                        paddr = self._aspace.vtop(new_vaddr)
                        real_size = len(self._aspace.zread(new_vaddr, left_over))
                        self.__push(fm, offset, real_size, paddr)
                        offset += real_size
        except:
            traceback.print_exc()

    def __push(self, fm, offset, size, paddr):
        if paddr != None:
            try:
                fm.push(offset, size, self._fsobj.memdump, long(paddr), True)
            except:
                pass
        else:
            try:
                fm.push(offset, size, None, 0, True)
            except:
                pass


    def __round(self, addr, align, up=False):
        if addr % align == 0:
            return addr
        else:
            if up:
                return (addr + (align - (addr % align)))
            return (addr - (addr % align))
        

class DllNode(Node, WinMapper):
    def __init__(self, name, aspace, boffset, parent, fsobj):
        WinMapper.__init__(self)
        self._boffset = boffset
        self._fsobj = fsobj
        Node.__init__(self, name, 0, parent, fsobj)
        self.__disown__()
        self._aspace = aspace
        if aspace != None and aspace.is_valid_address(boffset):
            self._baseaddr = boffset
        fm = FileMapping(self)
        self.fileMapping(fm)
        self.setSize(fm.maxOffset())
        del fm


    def _attributes(self):
        attrs = VMap()
        if self._baseaddr != -1:
            attrs["Virtual Base address"] = Variant(self._boffset)
            attrs["Physical Base address"] = Variant(self._aspace.vtop(self._boffset))
        else:
            attrs["Virtual Base address (not valid addr)"] = Variant(self._boffset)
        return attrs

    @confswitch
    def fileMapping(self, fm):
        self._fileMapping(fm)



class ModuleNode(Node, WinMapper):
    def __init__(self, name, poffset, parent, fsobj, unlinked_or_hidden):
        WinMapper.__init__(self)
        address_space = utils.load_as(self._fsobj._config, astype = 'physical')
        kernel_as = utils.load_as(self.fsobj._config)
        self._poffset = poffset
        self._fsobj = fsobj
        Node.__init__(self, name, 0, parent, fsobj)
        self.__disown__()
        self._aspace = aspace
        if aspace != None and aspace.is_valid_address(boffset):
            self._baseaddr = boffset
        fm = FileMapping(self)
        self.fileMapping(fm)
        self.setSize(fm.maxOffset())
        del fm

    
    @confswitch
    def _attributes(self):
        attrs = VMap()
        if self._baseaddr != -1:
            attrs["Virtual Base address"] = Variant(self._boffset)
            attrs["Physical Base address"] = Variant(self._aspace.vtop(self._boffset))
        else:
            attrs["Virtual Base address (not valid addr)"] = Variant(self._boffset)
        return attrs


    @confswitch
    def fileMapping(self, fm):
        self._fileMapping(fm)


class WinProcNode(Node, WinMapper):
    #filename = lambda handle : handle.dereference_as("_FILE_OBJECT").file_name_with_device()
    #keyname = lambda handle : handle.dereference_as("_CM_KEY_BODY").full_key_name()
    #procname = lambda handle : handle.dereference_as("_EPROCESS").ImageFileName
    #thrdname = lambda handle : handle.dereference_as("_ETHREAD").Cid.UniqueThread
    handleMapper = {"Thread": "_setThreadAttributes",
                    "File": "_setFileAttributes",
                    "Key": "_setKeyAttributes"}
                        
    
    def __init__(self, eproc, offset, parent, fsobj):
        WinMapper.__init__(self)
        self.v = vfs()
        self.__offset = offset
        self.__pefile = None
        self.eproc = eproc
        self._aspace = self.eproc.get_process_address_space()
        self._fsobj = fsobj
        Node.__init__(self, str(self.eproc.ImageFileName), 0, parent, fsobj)
        self.__disown__()
        if self._aspace is not None and self.eproc.Peb is not None and self._aspace.is_valid_address(self.eproc.Peb.ImageBaseAddress):
            self._baseaddr = self.eproc.Peb.ImageBaseAddress
        else:
            self._baseaddr = -1
        self._setHandles()
        fm = FileMapping(self)
        self.fileMapping(fm)
        self.setSize(fm.maxOffset())
        del fm


    def _setKeyAttributes(self, handle, keys):
        keybody = handle.dereference_as("_CM_KEY_BODY")
        #vm = VMap()
        #vm["BaseBlockFileName"] = Variant(str(keybody.KeyControlBlock.KeyHive.BaseBlock.FileName))
        keys[keybody.full_key_name()] = Variant("")
        

    def _setThreadAttributes(self, handle, threads):
        thrd_attrs = VMap()

        thrd = handle.dereference_as("_ETHREAD")
        thrd_attrs["UniqueProcess"] = Variant(int(thrd.Cid.UniqueProcess))
        self._setTimestamp(thrd, thrd_attrs)
        threads[str(thrd.Cid.UniqueThread)] = thrd_attrs


    def _setFileAttributes(self, handle, files):
        file_attrs = VMap()

        fileobj = handle.dereference_as("_FILE_OBJECT")
        #self._setTimestamp(thrd, thrd_attrs)
        fnamedev = fileobj.file_name_with_device()
        if True:
            if fnamedev.find("\\Device\\HarddiskVolume1") != -1:
                fnamedev_overlay = fnamedev.replace("\\Device\\HarddiskVolume1", "WinXpPro/WinXpPro.vmdk/Baselink/VirtualHDD/Partitions/Partition 1/NTFS").replace("\\", "/")
                node = self.v.getnode(fnamedev_overlay)
                if node:
                    file_attrs["HardDriveImage"] = Variant(node)
                else:
                    file_attrs["HardDriveImage"] = Variant("Not found")
        file_attrs["WriteAccess"] = Variant(fileobj.WriteAccess > 0, typeId.Bool)
        file_attrs["ReadAccess"] = Variant(fileobj.ReadAccess > 0, typeId.Bool)
        file_attrs["DeleteAccess"] = Variant(fileobj.DeleteAccess > 0, typeId.Bool)
        file_attrs["SharedRead"] = Variant(fileobj.SharedRead > 0, typeId.Bool)
        file_attrs["SharedWrite"] = Variant(fileobj.SharedWrite > 0, typeId.Bool)
        file_attrs["SharedDelete"] = Variant(fileobj.SharedDelete > 0, typeId.Bool)
        files[fnamedev] = file_attrs



    def _setHandles(self):
        self.handles_map = VMap()
        hmap = {}
        for handle in self.eproc.ObjectTable.handles():
            object_type = handle.get_object_type()
            if object_type != None:
                if object_type in WinProcNode.handleMapper:
                    if object_type not in hmap:
                        hmap[str(object_type)] = VMap()
                    func = getattr(self, WinProcNode.handleMapper[object_type])
                    func(handle, hmap[str(object_type)])
                else:
                    pass
                    #name = str(handle.NameInfo.Name)
                    #     if len(name):
                    #if object_type not in self.handles_map:
                    #    self.handles_map[object_type] = []
                    #self.handles_map[object_type].append(name)
        for key in hmap:
            self.handles_map[key] = hmap[key]


    def _setTimestamp(self, obj, attrs):
        if obj.ExitTime:
            exit_datetime = obj.ExitTime.as_windows_timestamp()
            vt = vtime(exit_datetime, TIME_MS_64)
            vt.thisown = False
            attrs["State"] = Variant("Exited")
            attrs["Exit time"] = Variant(vt)
        else:
            attrs["State"] = Variant("Running")
        create_datetime = obj.CreateTime.as_windows_timestamp()
        vt = vtime(create_datetime, TIME_MS_64)
        vt.thisown = False
        attrs["Create time"] = Variant(vt)


    def _setProcessParameters(self, attrs):
        proc_params = self.eproc.Peb.ProcessParameters
        params_attrs = VMap()
        params_attrs["ImagePathName"] = Variant(str(proc_params.ImagePathName))
        params_attrs["CommandLine"] = Variant(str(proc_params.CommandLine))
        attrs["Process Parameters"] = params_attrs


    def _setImportedFunctions(self, name, attrs):
        if self.__pe and hasattr(self.__pe, "DIRECTORY_ENTRY_IMPORT"):
            found = False
            for entry in self.__pe.DIRECTORY_ENTRY_IMPORT:
                if name.lower().find(entry.dll.lower()) != -1:
                    found = True
                    break
            if found:
                funcs = VList()
                for imp in entry.imports:
                    func = VMap()
                    if imp.name:
                        func[str(imp.name)] = Variant(imp.address)
                    else:
                        func[str(imp.ordinal)] = Variant(imp.address)
                    funcs.append(func)
                attrs["Imported functions"] = Variant(funcs)


    def _setLoadedModules(self, attrs):
        dlls = VList()
        for m in self.eproc.get_load_modules():
            name = str(m.FullDllName) or 'N/A'
            dll = VMap()
            dllattribs = VMap()
            dllattribs["Base"] = Variant(long(m.DllBase))
            dllattribs["Size"] = Variant(long(m.SizeOfImage))
            if name != "N/A":
                self._setImportedFunctions(name, dllattribs)
            dll[name] = Variant(dllattribs)
            dlls.append(dll)
            attrs["Loaded modules"] = Variant(dlls)


    def __setConnections(self, attrs):
        if self._fsobj.connections.has_key(long(self.eproc.UniqueProcessId)):
            conns = VMap()
            count = 0
            for conn_obj in self._fsobj.connections[long(self.eproc.UniqueProcessId)]:
                count += 1
                conn = VMap()
                conn["Local IP address"] = Variant(str(conn_obj.localAddr))
                conn["Local port"] = Variant(int(conn_obj.localPort))
                if conn_obj.proto is not None:
                    conn["Protocol"] = Variant(int(conn_obj.proto))
                conn["Protocol type"] = Variant(conn_obj.type)
                if conn_obj.ctime is not None:
                    create_datetime = conn_obj.ctime.as_windows_timestamp()
                    vt = vtime(create_datetime, TIME_MS_64)
                    vt.thisown = False
                    conn["Create time"] = Variant(vt)
                if conn_obj.remoteAddr is not None:
                    conn["Remote IP address"] = Variant(str(conn_obj.remoteAddr))
                    conn["Remote port"] = Variant(int(conn_obj.remotePort))
                if conn_obj.state is not None:
                    conn["State"] = Variant(str(conn_obj.state))
                conns["Connection " + str(count)] = Variant(conn)
            attrs["Connections"] = conns
        
    
    @confswitch
    def fileMapping(self, fm):
        self._fileMapping(fm)
        

    @confswitch
    def _attributes(self):
        try:
            if PEFILE_FOUND:
                f = self.open()
                buff = f.read()
                f.close()
                try:
                    self.__pe = pefile.PE(data=buff)
                except:
                    self.__pe = None
            attrs = VMap()
            attrs["PID"] = Variant(int(self.eproc.UniqueProcessId))
            attrs["Parent PID"] = Variant(int(self.eproc.InheritedFromUniqueProcessId))
            attrs["Active Threads"] = Variant(int(self.eproc.ActiveThreads))
            if self.eproc.Peb:
                self._setLoadedModules(attrs)
            for source in self._fsobj.ps_sources:
                attrs[source] = Variant(self._fsobj.ps_sources[source].has_key(self.__offset), typeId.Bool)
            self.__setConnections(attrs)
            hcount = int(self.eproc.ObjectTable.HandleCount)
            if hcount < 0:
                hcount = 0
            attrs["Handle Count"] = Variant(hcount)
            if self.eproc.Peb == None:
                attrs["PEB"] = Variant("at " + hex(self.eproc.m('Peb')) + " is paged")
            elif self._aspace.vtop(self.eproc.Peb.ImageBaseAddress) == None:
                attrs["ImageBaseAddress"] = Variant("at " + hex(self.eproc.Peb.ImageBaseAddress) + " is paged")
            self._setProcessParameters(attrs)
            self._setTimestamp(self.eproc, attrs)
            attrs["Handles"] = self.handles_map
        except:
            import traceback
            traceback.print_exc()

        return attrs