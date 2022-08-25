from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import auth
import datetime
from frappe.utils import getdate
import json, ast, requests
import urllib.request

class SupportTicket(Document):
	@frappe.whitelist()
	def before_validate(self):
		self.fetch_employee_contacts()

	@frappe.whitelist()
	def validate(self):
		high_priority = frappe.db.sql(""" select name as name, count(name) as count from `tabSupport Ticket` where priority = "High" and status != "Closed" """, as_dict=1)
		for x in high_priority:
			if self.priority == "High" and x.count > 0 and self.name != x.name:
				frappe.throw("You Already Have A High Priority Ticket #" + x.name)

	@frappe.whitelist()
	def after_insert(self):
		self.create_issue()

	@frappe.whitelist()
	def on_update(self):
		self.update_issue()

	@frappe.whitelist()
	def fetch_employee_contacts(self):
		user = frappe.session.user
		support_user = frappe.db.get_value("Support User", user, "name")
		if not support_user:
			frappe.throw("Please Create <a href=/app/support-user>Support User</a> With Your AnyDesk ID, Mobile No & Email Address, So That We Can Contact You After Resolving Your Ticket.")
		self.anydesk_id = frappe.db.get_value("Support User", user, "anydesk_id")
		self.mobile_no = frappe.db.get_value("Support User", user, "mobile_no")
		self.email = frappe.db.get_value("Support User", user, "email")

	@frappe.whitelist()
	def create_issue(self):
		remote_system_url = frappe.db.get_single_value("Support Ticket Settings", "remote_system_url")
		api_key = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_key")
		api_secret = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_secret")
		token = api_key + ":" + api_secret
		authorization = 'token ' + token
		data = {}
		data["doctype"] = "Issue"
		data["ticket_no"] = self.name
		data["system_url"] = frappe.db.get_single_value("Support Ticket Settings", "system_url")
		data["project"] = frappe.db.get_single_value("Support Ticket Settings", "project_name")
		data["raised_by"] = self.email
		data["contact_person"] = self.name1
		data["anydesk_id"] = self.anydesk_id
		data["mobile_no"] = self.mobile_no
		data["email"] = self.email
		data["subject"] = self.subject
		data["opening_date"] = self.opening_date
		data["opening_time"] = self.opening_time
		data["status"] = self.status
		data["priority"] = self.priority
		data["issue_type"] = self.issue_type
		data["description"] = self.description
		data["support_rating"] = self.support_rating

		url = remote_system_url + '/api/method/ecs_ecs.functions.issue_add'
		headers = {'content-type': 'application/json; charset=utf-8', 'Accept': 'application/json',
				   'Authorization': authorization}
		response = requests.post(url, json=data, headers=headers)
		returned_data = json.loads(response.text)
		self.issue_no = returned_data['message']
		self.save()

	@frappe.whitelist()
	def update_issue(self):
		remote_system_url = frappe.db.get_single_value("Support Ticket Settings", "remote_system_url")
		api_key = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_key")
		api_secret = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_secret")
		token = api_key + ":" + api_secret
		authorization = 'token ' + token
		user = frappe.session.user
		if user != "support@erpcloud.systems":
			data = {
				"doctype": "Issue",
				"name": self.issue_no,
				"ticket_no": self.name,
				"project": frappe.db.get_single_value("Support Ticket Settings", "project_name"),
				"system_url": frappe.db.get_single_value("Support Ticket Settings", "system_url"),
				"raised_by": self.email,
				"contact_person": self.name1,
				"anydesk_id": self.anydesk_id,
				"mobile_no": self.mobile_no,
				"email": self.email,
				"subject": self.subject,
				"opening_date": self.opening_date,
				"opening_time": self.opening_time,
				"status": self.status,
				"priority": self.priority,
				"issue_type": self.issue_type,
				"description": self.description,
				"support_rating": self.support_rating
			}

			#frappe.msgprint(json.dumps(data))
			url = remote_system_url + '/api/method/ecs_ecs.functions.issue_update'
			headers = {'content-type': 'application/json; charset=utf-8', 'Accept': 'application/json',
					   'Authorization': authorization}
			response = requests.put(url, json=data, headers=headers)
			returned_data = json.loads(response.text)
			#frappe.msgprint(returned_data['message'])
			#frappe.msgprint(returned_data)

