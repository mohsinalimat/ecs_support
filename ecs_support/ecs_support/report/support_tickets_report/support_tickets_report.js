// Copyright (c) 2022, ERP Cloud Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Support Tickets Report"] = {
		"filters": [
        {
			"fieldname":"ticket_no",
			"label": __("Ticket No"),
			"fieldtype": "Link",
			"options":  "Support Ticket",
		},
		{
			"fieldname":"raised_by",
			"label": __("Raised By"),
			"fieldtype": "Link",
			"options":  "User",
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
		},
        {
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options":  ["", "Open", "Working","Replied", "Hold", "Resolved", "Closed"],
		},
        {
			"fieldname":"priority",
			"label": __("Priority"),
			"fieldtype": "Select",
			"options":  ["","Low", "Medium", "High"],
		},
		{
			"fieldname":"issue_type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options":  ["","استفسار", "طلب", "مشكلة","صلاحية"],
		},
	]
};
