# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters,columns)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Ticket No"),
			"fieldname": "ticket_no",
			"fieldtype": "Link",
			"options": "Support Ticket",
			"width": 110
		},
		{
			"label": _("Reference No"),
			"fieldname": "issue_no",
			"fieldtype": "Data",
			"width": 110
		},
		{
			"label": _("Raised By"),
			"fieldname": "name1",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Date"),
			"fieldname": "opening_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Time"),
			"fieldname": "opening_time",
			"fieldtype": "Time",
			"width": 90
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 90
		},
		{
			"label": _("Priority"),
			"fieldname": "priority",
			"fieldtype": "Data",
			"width": 90
		},
		{
			"label": _("Type"),
			"fieldname": "issue_type",
			"fieldtype": "Data",
			"width": 90
		},
		{
			"label": _("Subject"),
			"fieldname": "subject",
			"fieldtype": "Data",
			"width": 300
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("ticket_no"):
		conditions += " and a.name=%(ticket_no)s"
	if filters.get("raised_by"):
		conditions += " and a.raised_by=%(raised_by)s"
	if filters.get("from_date"):
		conditions += " and a.opening_date>=%(from_date)s"
	if filters.get("to_date"):
		conditions += " and a.opening_date<=%(to_date)s"
	if filters.get("status"):
		conditions += " and a.status=%(status)s"
	if filters.get("priority"):
		conditions += " and a.priority=%(priority)s"
	if filters.get("issue_type"):
		conditions += " and a.issue_type=%(issue_type)s"

	item_results = frappe.db.sql("""
				select
					a.name as ticket_no,
					a.issue_no as issue_no,
					a.name1 as name1,
					a.subject as subject,
					a.opening_date as opening_date,
					a.opening_time as opening_time,
					a.status as status,
					a.priority as priority,
					a.issue_type as issue_type,
					a.anydesk_id as anydesk_id,
					a.mobile_no as mobile_no,
					a.email as email				
				from `tabSupport Ticket` a 
				where
					a.docstatus = 0
					{conditions}
				order by
					a.name desc
				""".format(conditions=conditions), filters, as_dict=1)

	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'ticket_no': item_dict.ticket_no,
				'issue_no': item_dict.issue_no,
				'name1': item_dict.name1,
				'subject': item_dict.subject,
				'opening_date': item_dict.opening_date,
				'opening_time': item_dict.opening_time,
				'status': item_dict.status,
				'priority': item_dict.priority,
				'issue_type': item_dict.issue_type,
				'anydesk_id': item_dict.anydesk_id,
				'mobile_no': item_dict.mobile_no,
				'email': item_dict.email,
			}
			result.append(data)

	return result

