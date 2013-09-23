/*
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009-2013 ArxSys
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

#include "partition.hpp"

void Partition::start(std::map<std::string, Variant_p > args)
{
  std::map<std::string, Variant_p >::iterator	it;
  uint32_t					sectsize;
  uint64_t					soffset;

  soffset = 0;
  sectsize = 512;
  if ((it = args.find("sector-size")) != args.end())
    sectsize = it->second->value<uint32_t>();
  if ((it = args.find("offset")) != args.end())
    soffset = it->second->value<uint64_t>();
  if ((it = args.find("file")) != args.end())
    {
      try
	{
	  this->__parent = it->second->value<Node*>();
	  if (this->__parent->size() != 0)
	    {
	      this->__root = new PartitionsNode(this);
	      if (this->__dos->process(this->__parent, soffset, sectsize) && !this->__dos->isProtective())
		{
		  this->__dos->makeNodes(this->__root, this);
		  this->res = this->__dos->result();
		}	      
	      // XXX currently only take into account that provided offset
	      // includes protective / hybrid MBR
	      else if (this->__gpt->process(this->__parent, soffset, sectsize))
	      	{
	      	  this->__gpt->makeNodes(this->__root, this);
		  if (this->__dos->entriesCount() > 1)
		    this->res["Hybrid MBR"] = new Variant(this->__dos->result());
		  else
		    this->res["Protective MBR"] = new Variant(this->__dos->result());
	      	  this->res["GPT entries"] = new Variant(this->__gpt->result());
	      	}
	      this->registerTree(this->__parent, this->__root);
	    }
	}
      catch(vfsError e)
	{
	  delete this->__root;
	  throw vfsError("[PARTITION] error while processing file\n" + e.error);
	}
    }
  else
    throw envError("[PARTITION] file argument not provided\n");
}


Partition::Partition(): mfso("partition")
{
  this->__dos = new DosPartition();
  this->__gpt = new GptPartition();
}


Partition::~Partition()
{
  //Free All Memory !!!
  std::cout << "Dump Closed successfully" << std::endl;
}


PartitionsNode::PartitionsNode(Partition* fsobj) : Node("Partitions", 0, NULL, fsobj)
{
  this->__part = fsobj;
}


PartitionsNode::~PartitionsNode()
{
  
}


std::string PartitionsNode::icon()
{
  return std::string(":database");
}


Attributes	PartitionsNode::_attributes()
{
  return this->__part->res;
}
