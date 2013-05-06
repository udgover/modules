# Copyright (C) 2009-2011 ArxSys
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
#  Samuel CHEVET <gw4kfu@gmail.com>
#  Frederic Baguelin <fba@digital-forensic.org>
#

__dff_module_volatility_version__ = "1.0.0"

VOLATILITY_PATH = "/home/udgover/sources/volatility"
#VOLATILITY_PATH = "/home/udgover/sources/volatility-"

import sys
import os
import traceback


from dff.api.module.module import Module
from dff.api.vfs.libvfs import mfso, AttributesHandler, Node
from dff.api.types.libtypes import Variant, VMap, VList, typeId, Argument, Parameter, vtime, TIME_MS_64

from collections import namedtuple

debug = False

if VOLATILITY_PATH:
   sys.path.append(VOLATILITY_PATH)
try:
   from dff.modules.ram.addrspace import dffvol
   import volatility.conf as conf
   import volatility.timefmt as timefmt
   import volatility.registry as registry
   import volatility.obj as obj
   import volatility.utils as utils
   import volatility.addrspace as addrspace
   import volatility.commands as commands

   import volatility.win32.tasks as tasks
   import volatility.plugins.kdbgscan as kdbgscan
   import volatility.plugins.imageinfo as imageinfo
   import volatility.plugins.taskmods as taskmods
   import volatility.plugins.netscan as netscan
   import volatility.plugins.sockscan as sockscan
   import volatility.plugins.connscan as connscan
   import volatility.protos as protos

   import volatility.plugins.malware.psxview as psxview
   
   #import volatility.registry as registry
   import volatility.win32.network as network
   
   with_volatility = True
   config = conf.ConfObject()
   registry.PluginImporter()
   registry.register_global_options(config, addrspace.BaseAddressSpace)
   registry.register_global_options(config, commands.Command)

except ImportError:
   traceback.print_exc()
   with_volatility = False


from winproc import WinProcNode, DllNode

import time


class WinRootNode(Node):
   def __init__(self, name, parent, fsobj):
      Node.__init__(self, name, 0, None, fsobj)
      self.__fsobj = fsobj
      self._kdbg = self.__fsobj._kdbg
      self._aspace = self.__fsobj._aspace
      self.setDir()
      self.__disown__()


   def _attributes(self):
      attribs = VMap()
      kdbg_offsets = VMap()
      proc_head = VMap()
      mod_head = VMap()
      sys_info = VMap()

      sys_info["Chosen profile"] = Variant(self.__fsobj._config.PROFILE)
      sys_info["Major"] = Variant(self._kdbg.obj_vm.profile.metadata.get('major', 0))
      sys_info["Minor"] = Variant(self._kdbg.obj_vm.profile.metadata.get('minor', 0))
      sys_info["Build"] = Variant(self._kdbg.obj_vm.profile.metadata.get('build', 0))
      
      if hasattr(self._kdbg.obj_vm, 'vtop'):
         kdbg_offsets["virtual"] =  Variant(self._kdbg.obj_offset)
         kdbg_offsets["physical"] = Variant(self._kdbg.obj_vm.vtop(self._kdbg.obj_offset))
         sys_info["Service Pack (CmNtCSDVersion)"] = Variant(self._kdbg.ServicePack)
         sys_info["Build string (NtBuildLab)"] = Variant(str(self._kdbg.NtBuildLab.dereference()))
         try:
            num_tasks = len(list(self._kdbg.processes()))
         except AttributeError:
            num_tasks = 0
         try:
            num_modules = len(list(self._kdbg.modules()))
         except AttributeError:
            num_modules = 0
         cpu_blocks = list(self._kdbg.kpcrs())
         
         proc_head["offset"] = Variant(long(self._kdbg.PsActiveProcessHead))
         proc_head["process count"] = Variant(num_tasks)
         mod_head["offset"] = Variant(long(self._kdbg.PsLoadedModuleList))
         mod_head["modules count"] = Variant(num_modules)
         try:
            dos_header = obj.Object("_IMAGE_DOS_HEADER", offset = self._kdbg.KernBase, vm = self._kdbg.obj_vm)
            nt_header = dos_header.get_nt_header()
         except:
            pass
         else:
            sys_info["Major (OptionalHeader)"] = Variant(long(nt_header.OptionalHeader.MajorOperatingSystemVersion))
            sys_info["Minor (OptionalHeader)"] = Variant(long(nt_header.OptionalHeader.MinorOperatingSystemVersion))
         i = 0
         kpcrs = VMap()
         for kpcr in cpu_blocks:
            kpcrs["CPU " + str(kpcr.ProcessorBlock.Number)] = Variant(kpcr.obj_offset)
         attribs["KPCR(s)"] = Variant(kpcrs)
         attribs["DTB"] = Variant(self._aspace.dtb)
         volmagic = obj.VolMagic(self._aspace)
         KUSER_SHARED_DATA = volmagic.KUSER_SHARED_DATA.v()
         if KUSER_SHARED_DATA:
            attribs["KUSER_SHARED_DATA"] = Variant(KUSER_SHARED_DATA)
            k = obj.Object("_KUSER_SHARED_DATA",
                           offset = KUSER_SHARED_DATA,
                           vm = self._aspace)
            if k:
               stime = k.SystemTime
               vtstime = vtime(stime.as_windows_timestamp(), TIME_MS_64)
               vtstime.thisown = False
               attribs["Image date and time"] = Variant(vtstime)
               tz = timefmt.OffsetTzInfo(-k.TimeZoneBias.as_windows_timestamp() / 10000000)
               lsystime = stime.as_datetime().astimezone(tz)
               vtlstime = vtime(lsystime.year, lsystime.month, lsystime.day, lsystime.hour, lsystime.minute, lsystime.second, 0)
               vtlstime.thisown = False
               attribs["Image local date and time"] = Variant(vtlstime)
      else:
         kdbg_offsets["physical"] = Variant(self._kdbg.obj_offset)
         proc_head["offset"] = Variant(self._kdbg.PsActiveProcessHead)
         mod_head["offset"] = Variant(self._kdbg.PsLoadedModuleList)
      attribs["PsActiveProcessHead"] = Variant(proc_head)
      attribs["PsLoadedModuleList"] = Variant(mod_head)
      attribs["KDBG offsets"] = Variant(kdbg_offsets)
      attribs["KernelBase"] = Variant(long(self._kdbg.KernBase))
      if not hasattr(self._aspace, "pae"):
         attribs["PAE type"] = Variant("No PAE")
      else:
         attribs["PAE type"] = Variant("PAE")
      verinfo = self._kdbg.dbgkd_version64()
      if verinfo:
         ver64 = VMap()
         ver64["Major"] = Variant(long(verinfo.MajorVersion))
         ver64["Minor"] = Variant(long(verinfo.MinorVersion))
         ver64["offset"] = Variant(verinfo.obj_offset)
         sys_info["Version 64"] = Variant(ver64)
      attribs["System Information"] = Variant(sys_info)
      return attribs


class ConfigInstance(conf.ConfObject):
   # since Volatility's configuration is a singleton, we need to define a private configuration
   # per instance and update global configuration for context switching (from one instance to
   # another). Per instance's configuration is initialized with the following baseconf which
   # is itself based on ConfObject.default_opts dict. Then private configuration is updated
   # with profile information, kdbg offset and so on
   baseconf = {'profile': 'WinXPSP2x86',
               'use_old_as': None,
               'kdbg': None,
               'output_file': None,
               'tz': None,
               'verbose': None,
               'kpcr': None,
               'output': None,
               'dtb': 0,
               'cache': False,
               'conf_file': '',
               'filename': None,
               'write': False,
               'location': None,
               'debug': 0,
               'cache_dtb': False,
               'cache_directory': '',
               'addr_space': None}

   def __init__(self):
      conf.ConfObject.__init__(self)
      self.__context = {}
      self.__context.update(ConfigInstance.baseconf)
      for field in self.__context:
         try:
            self.update(field, self.__context[field])
         except:
            pass


   def updateCtx(self, key, value):
      self.__context[key.lower()] = value
      self.update(key, value)


   def switchContext(self):
      for field in self.__context:
         self.update(field, self.__context[field])


   def dump(self):
      for field in self.__context:
         print field, self.__context[field], self.get_value(field)


class Volatility(mfso):
   def __init__(self):
      mfso.__init__(self, "volatility")
      self.__disown__()
      self._config = ConfigInstance()

   def start(self, args):
      if not with_volatility:
         raise RuntimeError("Volatility not found. Please install it")
      self.memdump = args["file"].value()
      self._config.updateCtx('location', "file://" + self.memdump.absolute())
      self._config.updateCtx('filename', self.memdump.name())
      self._config.updateCtx('debug', True)
      self.__dlls = {}
      starttime = time.time()
      if args.has_key("profile"):
         self._config.updateCtx('profile', args['profile'].value())
         self._aspace = utils.load_as(self._config)
         self._kdbg = tasks.get_kdbg(self._aspace)
         self._config.updateCtx('kdbg', self._kdbg.obj_offset)
      else:
         try:
            self.__guessProfile()
         except:
            traceback.print_exc()
      try:
         self.root = WinRootNode("Windows RAM", self.memdump, self)
         self.__psxview = psxview.PsXview(self._config)
         self.__findProcesses()
         self.__createProcessTree()
         self.__createDlls()
         self.__findConnections()
         self.registerTree(self.memdump, self.root)
      except:
         traceback.print_exc()
      aspace = self._aspace
      count = 0
      if debug:
         while aspace:
            count += 1
            print 'AS Layer', str(count), aspace.__class__.__name__, "(", aspace.name, ")"
            aspace = aspace.base
         print time.time() - starttime



   def __guessProfile(self):
      bestguess = None
      profiles = [ p.__name__ for p in registry.get_plugin_classes(obj.Profile).values() ]
      scan_kdbg = kdbgscan.KDBGScan(self._config)
      suglist = []
      suglist = [ s for s, _ in scan_kdbg.calculate() ]
      if suglist:
         bestguess = suglist[0]
      if bestguess in profiles:
         profiles = [bestguess] + profiles
      chosen = 'none'
      for profile in profiles:
         self._config.updateCtx('profile', profile)
         addr_space = utils.load_as(self._config, astype='any')
         if hasattr(addr_space, 'dtb'):
            chosen = profile
            break
      if debug and bestguess != chosen:
         print bestguess, chosen
      volmagic = obj.VolMagic(addr_space)
      kdbgoffset = volmagic.KDBG.v()
      self._kdbg = obj.Object("_KDDEBUGGER_DATA64", offset = kdbgoffset, vm = addr_space)
      self._config.updateCtx('kdbg', self._kdbg.obj_offset)
      self._aspace = addr_space


   #this method does exactly the same as calculate method in psxview malware plugins
   # but as we don't need to yield each result, just create the ps_sources dict
   def __findProcesses(self):
      all_tasks = list(tasks.pslist(self._aspace))
      self.ps_sources = {}
      self.ps_sources['pslist'] = self.__psxview.check_pslist(all_tasks)
      self.ps_sources['psscan'] = self.__psxview.check_psscan()
      self.ps_sources['thrdproc'] = self.__psxview.check_thrdproc(self._aspace)
      self.ps_sources['csrss'] = self.__psxview.check_csrss_handles(all_tasks)
      self.ps_sources['pspcid'] = self.__psxview.check_pspcid(self._aspace)


   def __findRootProcesses(self, procmap):
      for pid in procmap.keys():
         for proc in procmap[pid]:
            if proc[0].InheritedFromUniqueProcessId not in procmap.keys():
               yield proc


   def __createPtree(self, procmap, ppid, parent):
      for pid in procmap.keys():
         for proc, offset in procmap[pid]:
            if int(proc.InheritedFromUniqueProcessId) == ppid:
               self.__orphaned[proc] = 1
               procnode = WinProcNode(proc, offset, parent, self)
               if proc.Peb != None:
                  __aspace = proc.get_process_address_space()
                  for mod in proc.get_load_modules():
                     paddr = -1
                     dllname = str(mod.BaseDllName)
                     if __aspace is not None and __aspace.is_valid_address(mod.DllBase.v()):
                        paddr = long(__aspace.vtop(mod.DllBase.v()))
                     if not self.__dlls.has_key(dllname):
                        self.__dlls[dllname] = [(paddr, __aspace, mod.DllBase.v(), [procnode])]
                     else:
                        exists = False
                        for item in self.__dlls[dllname]:
                           if paddr == item[0]:
                              exists = True
                              break
                        if exists:
                           item[3].append(procnode)
                        else:
                           self.__dlls[dllname].append((paddr, __aspace, mod.DllBase.v(), [procnode]))
               self.__createPtree(procmap, int(proc.UniqueProcessId), procnode)


   def __createDlls(self):
      if len(self.__dlls):
         self.__mainDllNode = Node("Dlls", 0, self.root, self)
         self.__mainDllNode.setDir()
         self.__mainDllNode.__disown__()
         for dllname in self.__dlls:
            if len(self.__dlls[dllname]) > 1:
               if debug:
                  print dllname, [entry[0] for entry in self.__dlls[dllname]]
               i = 0
               for entry in self.__dlls[dllname]:
                  if entry[0] != -1:
                     if i == 0:
                        dllnode = DllNode(dllname, entry[1], entry[2], self.__mainDllNode, self)
                        dllnode.__disown__()
                     else:
                        dllnode = DllNode(dllname+"-"+str(i), entry[1], entry[2], self.__mainDllNode, self)
                        dllnode.__disown__()
                     i += 1
            else:
               entry = self.__dlls[dllname][0]
               dllnode = DllNode(dllname, entry[1], entry[2], self.__mainDllNode, self)
               dllnode.__disown__()


   def __createProcessTree(self):
      seen_offsets = []
      procmap = {}
      self.__orphaned = {}
      for source in self.ps_sources.values():
         for offset in source.keys():
            if offset not in seen_offsets:
               seen_offsets.append(offset)
               cproc = source[offset]
               uid = int(cproc.UniqueProcessId)
               if procmap.has_key(uid):
                  dtb = []
                  for _proc in procmap[uid]:
                     if cproc.ImageFileName == _proc[0].ImageFileName and cproc.Pcb.DirectoryTableBase == _proc[0].Pcb.DirectoryTableBase:
                        dtb.append(_proc)
                  if len(dtb) == 0:
                     procmap[uid].append((cproc, offset))
                  elif cproc.Peb != None:
                     for _proc in dtb:
                        if _proc.Peb is None:
                           procmap[uid].remove(_proc)
               else:
                  procmap[uid] = [(cproc, offset)]
               self.__orphaned[cproc] = 0
      if len(procmap):
         self.__mainProcNode = Node("Processes", 0, self.root, self)
         self.__mainProcNode.__disown__()
         self.__mainProcNode.setDir()
         for proc, offset in self.__findRootProcesses(procmap):
            self.__orphaned[proc] = 1
            procnode = WinProcNode(proc, offset, self.__mainProcNode, self)
            self.__createPtree(procmap, int(proc.UniqueProcessId), procnode)
         for proc in self.__orphaned:
            if debug and self.__orphaned[proc] == 0:
               self.__printProcess(proc)


   def __findConnections(self):
      self.connections = {}
      conn = namedtuple("aconn", ['localAddr', 'localPort', 'proto', 'type', 'ctime', 'remoteAddr', 'remotePort', 'state'])
      if self._aspace.profile.metadata.get('major', 0) == 6:
         for net_object, proto, laddr, lport, raddr, rport, state in netscan.Netscan(self._config).calculate():
            if proto.startswith("UDP"):
               raddr = rport = None
            if not self.connections.has_key(long(net_object.Owner.UniqueProcessId)):
               self.connections[long(net_object.Owner.UniqueProcessId)] = [conn(laddr, lport, None, proto, net_object.CreateTime or None, raddr, rport, state)]
            else:
               self.connections[long(net_object.Owner.UniqueProcessId)].append(conn(laddr, lport, None, proto, net_object.CreateTime or None, raddr, rport, state))
                                                                          
      else:
         socks = {}
         conns = {}
         for tcp_obj in connscan.ConnScan(self._config).calculate():
            if not conns.has_key(long(tcp_obj.Pid)):
               conns[long(tcp_obj.Pid)] = {long(tcp_obj.LocalPort): [tcp_obj]}
            elif not conns[long(tcp_obj.Pid)].has_key(long(tcp_obj.LocalPort)):
               conns[long(tcp_obj.Pid)][long(tcp_obj.LocalPort)] = [tcp_obj]
            else:
               conns[long(tcp_obj.Pid)][long(tcp_obj.LocalPort)].append(tcp_obj)
         for sock_obj in sockscan.SockScan(self._config).calculate():
            if not socks.has_key(long(sock_obj.Pid)):
               socks[long(sock_obj.Pid)] = [sock_obj]
            else:
               socks[long(sock_obj.Pid)].append(sock_obj)
         for pid in socks:
            pconns = []
            for sock_obj in socks[pid]:
               if conns.has_key(pid) and conns[pid].has_key(long(sock_obj.LocalPort)):
                  for tcp_obj in conns[pid][long(sock_obj.LocalPort)]:
                     pconns.append(conn(tcp_obj.LocalIpAddress, tcp_obj.LocalPort, sock_obj.Protocol,
                                        protos.protos.get(sock_obj.Protocol.v(), "-"), sock_obj.CreateTime,
                                        tcp_obj.RemoteIpAddress, tcp_obj.RemotePort, None))
                  del conns[pid][long(sock_obj.LocalPort)]
               else:
                  pconns.append(conn(sock_obj.LocalIpAddress, sock_obj.LocalPort, sock_obj.Protocol,
                                     protos.protos.get(sock_obj.Protocol.v(), "-"), sock_obj.CreateTime,
                                     None, None, None))
            self.connections[pid] = pconns
         for pid in conns:
            if len(conns[pid]):
               for port in conns[pid]:
                  for tcp_obj in conns[pid][port]:
                     self.connections[pid].append(conn(tcp_obj.LocalIpAddress, tcp_obj.LocalPort, 6, "TCP", None, 
                                                       tcp_obj.RemoteIpAddress, tcp_obj.RemotePort, None))
         if debug:
            for pid in self.connections:
               print "PID", pid
               for pconn in self.connections[pid]:
                  print "\t", pconn


   def __printProcess(self, proc):
      print "{name:<30}{uid:<10}{puid:<10}{stime:<30}{etime:<30}{cr3:<15}".format(name=proc.ImageFileName, uid=proc.UniqueProcessId, puid=proc.InheritedFromUniqueProcessId, stime=proc.CreateTime, etime=proc.ExitTime, cr3=hex(proc.Pcb.DirectoryTableBase))



class mvolatility(Module):
   """Analyse windows ram dump"""
   def __init__(self):
      if not with_volatility:
         raise RuntimeError("Volatility not found. Please install it")
      Module.__init__(self, "mvolatility", Volatility)
      self.conf.addArgument({"name": "file",
                             "description": "Dump to analyse",
                             "input": Argument.Required|Argument.Single|typeId.Node
                             })

      self.conf.addArgument({"name": "hdd_base",
                             "description": "Hard Disk Drive mount point associated to this memory dump",
                             "input": Argument.Optional|Argument.Single|typeId.Node
                             })

      self.conf.addArgument({"name": "profile",
                             "description": "Profile to use",
                             "input": Argument.Optional|Argument.Single|typeId.String,
                             "parameters": {"type": Parameter.NotEditable,
                                            "predefined": [ p.__name__ for p in registry.get_plugin_classes(obj.Profile).values() ]}
                             })
      self.conf.description = "Analyse windows ram dump"
      self.tags = "Volatile memory"
      self.icon = ":dev_ram.png"
