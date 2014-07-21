/*
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009-2014 ArxSys
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 *  
 * See http://www.digital-forensic.org for more information about this
 * project. Please do not directly contact any of the maintainers of
 * DFF for assistance; the project provides a web site, mailing lists
 * and IRC channels for your use.
 * 
 * Author(s):
 *  Frederic Baguelin <fba@digital-forensic.org>
 */

#include "volume.hpp"
#include "vfile.hpp"
#include "variant.hpp"

//#include "hfsbtree.hpp"


VolumeHeader::VolumeHeader()
{
}


VolumeHeader::~VolumeHeader()
{
}


void	displayFiles(fork_data forkdata, Node* node)
{
  // uint64_t	start;
  // uint64_t	count;
  // uint64_t	it;

  // VFile*	vf;
  // BtreeNode	bnode;
  // HeaderNode	hnode;
  // uint8_t*	buff;
  // kcatalog	cat;

  // uint8_t*	name;

  // name = (uint8_t*)malloc(sizeof(uint8_t) * 512);
  // buff = (uint8_t*)malloc(sizeof(uint8_t) * 4096);

  // vf = node->open();
  // start = (uint64_t)bswap32(forkdata.extents[0].startBlock);
  // start *= 4096;
  // count = (uint64_t)bswap32(forkdata.extents[0].blockCount);
  // std::cout << start << std::endl;
  // vf->seek(start);
  // vf->read(buff, 4096);
  // memcpy(&bnode, buff, sizeof(bnode));
  // memcpy(&hnode, buff+sizeof(bnode), sizeof(hnode));
  // uint16_t	swap16;
  // uint32_t	swap32;
  // if (bnode.kind == 1)
  //   std::cout << "Header node found" << std::endl;
  // else
  //   std::cout << "not header node :(" << std::endl;
  // swap16 = bswap16(bnode.numRecords);
  // std::cout << "record: " << swap16 << std::endl;
  // swap16 = bswap16(hnode.treeDepth);
  // std::cout << "depth: " << swap16 << std::endl;
  // swap32 = bswap32(hnode.totalNodes);
  // std::cout << "Total nodes: " << swap32 << std::endl;
  // swap16 = bswap16(hnode.maxKeyLength);
  // std::cout << "max key length: " << swap16 << std::endl;
  // for (it = 1; it < count; it++)
  //   {
  //     memset(buff, 0, 4096);
  //     vf->read(buff, 4096);
  //     memcpy(&bnode, buff, sizeof(bnode));
  //     //printf("node type: %d\n", bnode.kind);
  //     if (bnode.kind == -1)
  //     	{
  // 	  //std::cout << "Leaf node" << std::endl;
  //      	  memcpy(&cat, buff+sizeof(bnode), sizeof(cat));
  // 	  //std::cout << "prtou" << std::endl;
  //      	  memset(name, 0, 512);
  // 	  swap16 = bswap16(cat.keyLength);
  // 	  if (swap16 < 516 && swap16 > 6)
  //     	    {
  // 	      uint16_t len;
  // 	      memcpy(&len, buff+sizeof(bnode)+sizeof(cat), 2);
  // 	      len = bswap16(len);
  // 	      memset(name, 0, 512);
  //     	      memcpy(name, buff+sizeof(bnode)+sizeof(cat)+2, len*2);
  // 	      //for (int i = 1; i < len; i++)
  // 	      //printf("%c", name[i]);
  // 	      //printf("\n");
		  
  //     	    }
  //     	}
  //   }
}

void	VolumeHeader::process(Node* origin, fso* fsobj) throw (std::string)
{
  VFile*	vf;

  memset(&this->__vheader, 0, sizeof(volumeheader));
  if (origin == NULL)
    throw std::string("Provided node does not exist");
  try
    {
      vf = origin->open();
      vf->seek(1024);
      std::cout << "Reading " << sizeof(volumeheader) << " bytes at " << vf->tell() << std::endl;
      if (vf->read(&this->__vheader, sizeof(volumeheader)) != sizeof(volumeheader))
	{
	  vf->close();
	  delete vf;
	  throw std::string("Error while reading HFS Volume Header");
	}
    }
  catch (...)
    {
    }
}


Attributes	VolumeHeader::_attributes()
{
  Attributes	vmap;

  vmap["version"] = new Variant(this->version());
  vmap["last mounted version"] = new Variant(this->lastMountedVersion());
  vmap["created"] = new Variant(this->createDate());
  vmap["modified"] = new Variant(this->modifyDate());
  vmap["backup"] = new Variant(this->backupDate());
  vmap["checked"] = new Variant(this->checkedDate());
  vmap["Total number of files"] = new Variant(this->fileCount());
  vmap["Total number of folders"] = new Variant(this->folderCount());
  vmap["allocation block size"] = new Variant(this->blockSize());
  vmap["total number of allocation blocks"] = new Variant(this->totalBlocks());
  vmap["total number of free allocation blocks"] = new Variant(this->freeBlocks());
  vmap["total mounted"] = new Variant(this->writeCount());
  vmap["clump size for resource fork"] = new Variant(this->rsrcClumpSize());
  vmap["clump size for data fork"] = new Variant(this->dataClumpSize());
  return vmap;
}


uint16_t	VolumeHeader::signature()
{
  return bswap16(this->__vheader.signature);
}


uint16_t	VolumeHeader::version()
{
  return bswap16(this->__vheader.version);
}


uint32_t	VolumeHeader::attributes()
{
  return bswap32(this->__vheader.attributes);
}


uint32_t	VolumeHeader::lastMountedVersion()
{
  return bswap32(this->__vheader.lastMountedVersion);
}


uint32_t	VolumeHeader::journalInfoBlock()
{
  return bswap32(this->__vheader.journalInfoBlock);
}


vtime*		VolumeHeader::createDate()
{
  uint32_t	cdate;

  cdate = bswap32(this->__vheader.createDate);
  return new HfsVtime(cdate);  
}


vtime*		VolumeHeader::modifyDate()
{
  uint32_t	mdate;
    
  mdate = bswap32(this->__vheader.modifyDate);
  return new HfsVtime(mdate);
}


vtime*		VolumeHeader::backupDate()
{
  uint32_t	bdate;

  bdate = bswap32(this->__vheader.backupDate);
  return new HfsVtime(bdate);
}


vtime*		VolumeHeader::checkedDate()
{
  uint32_t	chkdate;

  chkdate = bswap32(this->__vheader.checkedDate);
  return new HfsVtime(chkdate);
}
 

uint32_t	VolumeHeader::fileCount()
{
  return bswap32(this->__vheader.fileCount);
}


uint32_t	VolumeHeader::folderCount()
{
  return bswap32(this->__vheader.folderCount);
}


uint32_t	VolumeHeader::blockSize()
{
  return bswap32(this->__vheader.blockSize);
}


uint32_t	VolumeHeader::totalBlocks()
{
  return bswap32(this->__vheader.totalBlocks);
}


uint32_t	VolumeHeader::freeBlocks()
{
  return bswap32(this->__vheader.freeBlocks);
}


uint32_t	VolumeHeader::nextAllocation()
{
  return bswap32(this->__vheader.nextAllocation);
}


uint32_t	VolumeHeader::rsrcClumpSize()
{
  return bswap32(this->__vheader.rsrcClumpSize);
}



uint32_t	VolumeHeader::dataClumpSize()
{
  return bswap32(this->__vheader.dataClumpSize);
}


uint32_t	VolumeHeader::nextCatalogID()
{
  return bswap32(this->__vheader.nextCatalogID);
}


uint32_t	VolumeHeader::writeCount()
{
  return bswap32(this->__vheader.writeCount);
}


uint64_t	VolumeHeader::encodingsBitmap()
{
  return bswap64(this->__vheader.encodingsBitmap);
}


fork_data	VolumeHeader::allocationFile()
{
  return this->__vheader.allocationFile;
}


fork_data	VolumeHeader::extentsFile()
{
  return this->__vheader.extentsFile;
}


fork_data	VolumeHeader::catalogFile()
{
  return this->__vheader.catalogFile;
}


fork_data	VolumeHeader::attributesFile()
{
  return this->__vheader.attributesFile;
}


fork_data	VolumeHeader::startupFile()
{
  return this->__vheader.startupFile;
}


bool	VolumeHeader::isHfspVolume()
{
  return (this->signature() == HfspVolume || this->version() == 4);
}


bool	VolumeHeader::isHfsxVolume()
{
  return (this->signature() == HfspVolume || this->version() == 5);
}


bool	VolumeHeader::createdByFsck()
{
  return (this->lastMountedVersion() == Fsck);
}


bool	VolumeHeader::isJournaled()
{
  return (this->lastMountedVersion() == Journaled 
	  || ((this->attributes() & VolumeJournaled) == VolumeJournaled));
}


bool	VolumeHeader::isMacOsX()
{
  return (this->lastMountedVersion() == MacOsX);
}


bool	VolumeHeader::isMacOs()
{
  return (this->lastMountedVersion() == MacOs);
}


bool	VolumeHeader::correctlyUmount()
{
  return (((this->attributes() & VolumeUmounted) == VolumeUmounted)
	  && ((this->attributes() & BootVolumeInconsistent) != BootVolumeInconsistent));
}


bool	VolumeHeader::hasBadBlocksExtents()
{
  return ((this->attributes() & VolumeSparedBlocks) == VolumeSparedBlocks);
}


bool	VolumeHeader::isRamDisk()
{
  return ((this->attributes() & VolumeNoCacheRequired) == VolumeNoCacheRequired);
}


bool	VolumeHeader::isCatalogIdReused()
{
  return ((this->attributes() & CatalogNodeIDsReused) == CatalogNodeIDsReused);
}


bool	VolumeHeader::isWriteProtected()
{
  return ((this->attributes() & VolumeSoftwareLock) == VolumeSoftwareLock);
}
