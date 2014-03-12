/*
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009-2011 ArxSys
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 *  
 * See http: *www.digital-forensic.org for more information about this
 * project. Please do not directly contact any of the maintainers of
 * DFF for assistance; the project provides a web site, mailing lists
 * and IRC channels for your use.
 * 
 * Author(s):
 *  Solal Jacob <sja@digital-forensic.org>
 */

#include "ntfs.hpp"
#include "ntfsopt.hpp"
#include "bootsector.hpp"
#include "mftentrynode.hpp"
#include "mftnode.hpp"

#include <iostream>

NTFS::NTFS() : __opt(NULL), __rootDirectoryNode(new Node("NTFS")), __bootSectorNode(NULL), mfso("NTFS")
{
}

NTFS::~NTFS()
{
  if (this->__bootSectorNode)
    delete this->__bootSectorNode;
  if (this->__rootDirectoryNode)
    delete this->__rootDirectoryNode;
}

void 		NTFS::start(Attributes args)
{
  this->__opt = new NTFSOpt(args);
  this->__bootSectorNode = new BootSectorNode(this);

  if (this->__opt->validateBootSector())
    this->__bootSectorNode->validate();

  this->setStateInfo("Reading main MFT");
  printf("size of MFTNode %d\n", sizeof(MFTNode)); 
  MFTNode* mftNode = new MFTNode(this, this->fsNode(), this->rootDirectoryNode(),  this->__bootSectorNode->MFTLogicalClusterNumber() * this->__bootSectorNode->clusterSize());

  uint64_t i = 0;
  uint64_t nMFT = mftNode->size() / 1024;

  std::ostringstream nMFTStream;
  nMFTStream  << std::string("Found ") << nMFT <<  std::string(" MFT entry") << endl;
  this->setStateInfo(nMFTStream.str());

  printf("sizeof MFTEntryNode %d\n", sizeof(MFTEntryNode));
  while (i * 1024 < mftNode->size())
  {
          //std::ostringstream cMFTStream;
     //cMFTStream << "Parsing " << i << "/" << nMFT << endl;
     //std::cout << cMFTStream.str() << std::endl;
     //this->setStateInfo(cMFTStream.str());
     MFTNode* currentMFTNode = new MFTNode(this, mftNode, this->rootDirectoryNode(), i * 1024);
     i += 1;
  }
  this->registerTree(this->opt()->fsNode(), this->rootDirectoryNode());

  this->setStateInfo("finished successfully");
  this->res["Result"] = Variant_p(new Variant(std::string("NTFS parsed successfully.")));
}

NTFSOpt*	NTFS::opt(void)
{
  return (this->__opt);
}

Node*		NTFS::fsNode(void)
{
  return (this->__opt->fsNode());
}

void 		NTFS::setStateInfo(const std::string info)
{
  this->stateinfo = info;
}

Node*		NTFS::rootDirectoryNode(void)
{
  return (this->__rootDirectoryNode);
}

BootSectorNode*	NTFS::bootSectorNode(void)
{
  return (this->__bootSectorNode);
}
