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

#include "pff.hpp"

PffNodeTask::PffNodeTask(std::string name, Node* parent, fso* fsobj, libpff_item_t* task, libpff_file_t** file, bool clone) : PffNodeEmailMessageText(name, parent, fsobj, task, file, clone)
{
}

std::string	PffNodeTask::icon(void)
{
  return (":tasks");
}

Attributes	PffNodeTask::_attributes(void)
{
  Attributes		attr;
  libpff_item_t*	item = NULL;
  libpff_error_t*       pff_error = NULL;
  
  //if (this->pff_item == NULL)
  //{
    if (libpff_file_get_item_by_identifier(*(this->pff_file), this->identifier, &item, &pff_error) != 1)
    {
      check_error(pff_error)
      std::cout << "pff node task can't get attribute " << std::endl;
      return attr;
    }
    //}
    //else 
    //item = *(this->pff_item);

  attr = this->allAttributes(item);
  Attributes	task;
  this->attributesTask(&task, item);
  attr[std::string("Task")] = new Variant(task);

  if (this->pff_item == NULL)
    if (libpff_item_free(&item, &pff_error) != 1)
      check_error(pff_error)

  return attr;
}

void	PffNodeTask::attributesTask(Attributes*	attr, libpff_item_t* item)
{
  libpff_error_t* pff_error                     = NULL;
  uint64_t	entry_value_64bit               = 0;
  uint32_t	entry_value_32bit               = 0;
  uint8_t	entry_value_boolean		= 0;
  double	entry_value_floating_point	= 0.0;
  int 		result                          = 0;

  value_time_to_attribute(libpff_task_start_date, "Start date")
  value_time_to_attribute(libpff_task_due_date, "Due date")
  value_uint32_to_attribute(libpff_task_get_status, "Status")
  
  result = libpff_task_get_percentage_complete(item, &entry_value_floating_point, &pff_error);
  if (result != -1 && result != 0)
  {
     std::ostringstream sfloat;

     sfloat << entry_value_floating_point;     
     (*attr)["Percentage complete"] = new Variant(sfloat.str());
  }
  else
    check_error(pff_error) 

  value_uint32_to_attribute(libpff_task_get_actual_effort, "Actual effort")
  value_uint32_to_attribute(libpff_task_get_total_effort, "Total effort")

  result = libpff_task_get_is_complete(item, &entry_value_boolean, &pff_error);
  if (result != -1 && result != 0)
  {
     if (entry_value_boolean)
       (*attr)["Is complete"] = new Variant(std::string("Yes"));
     else
       (*attr)["Is complete"] = new Variant(std::string("No"));
  }
  else
    check_error(pff_error) 
  value_uint32_to_attribute(libpff_task_get_version, "Version")
}
