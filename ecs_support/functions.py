from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import auth
import datetime
from frappe.utils import getdate
import json, ast, requests
import urllib.request


@frappe.whitelist()
def support_update(**kwargs):
	user = frappe.session.user
	if user == "support@erpcloud.systems":
		ticket = frappe.get_doc('Support Ticket', kwargs['ticket_no'])
		ticket.status = kwargs["status"]
		ticket.issue_type = kwargs["issue_type"]
		ticket.description = kwargs["description"]
		ticket.resolution_details = kwargs["resolution_details"]
		ticket.support_reply = kwargs["support_reply"]
		ticket.save()
		ticket_name = ticket.name

		if ticket_name:
			return "Issue Updated Successfully"
		else:
			return "Issue Not Updated"
