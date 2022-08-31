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

@frappe.whitelist()
def add_attachment(doc, method=None):
    remote_system_url = frappe.db.get_single_value("Support Ticket Settings", "remote_system_url")
    api_key = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_key")
    api_secret = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_secret")
    token = api_key + ":" + api_secret
    authorization = 'token ' + token
    user = frappe.session.user
    if user != "support@erpcloud.systems" and doc.attached_to_doctype == "Support Ticket":
        ticket = frappe.get_doc("Support Ticket", doc.attached_to_name)
        data = {
            "name": ticket.issue_no,
            "ticket_no": doc.attached_to_name,
            "file_url": doc.file_url,
            "file_name": doc.file_name,
            "system_url": frappe.db.get_single_value("Support Ticket Settings", "system_url"),
        }

        # frappe.msgprint(json.dumps(data))
        url = remote_system_url + '/api/method/ecs_ecs.functions.update_attachment'
        headers = {'content-type': 'application/json; charset=utf-8', 'Accept': 'application/json',
                   'Authorization': authorization}
        response = requests.put(url, json=data, headers=headers)
        returned_data = json.loads(response.text)
# frappe.msgprint(returned_data['message'])
# frappe.msgprint(returned_data)


@frappe.whitelist()
def add_comment(doc, method=None):
    user = frappe.session.user
    if user != "support@erpcloud.systems" and doc.reference_doctype == "Support Ticket":
        remote_system_url = frappe.db.get_single_value("Support Ticket Settings", "remote_system_url")
        api_key = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_key")
        api_secret = frappe.db.get_single_value("Support Ticket Settings", "ticket_api_secret")
        token = api_key + ":" + api_secret
        authorization = 'token ' + token
        data = {}
        data["doctype"] = "Comment"
        data["comment_type"] = "Comment"
        data["reference_doctype"] = "Issue"
        data["reference_name"] = frappe.db.get_value("Support Ticket", doc.reference_name, "issue_no")
        data["content"] = "<b>" + doc.comment_by + ": </b>" + doc.content
        data["comment_by"] = doc.comment_by

        url = remote_system_url + '/api/method/ecs_ecs.functions.update_comment'
        headers = {'content-type': 'application/json; charset=utf-8', 'Accept': 'application/json',
                   'Authorization': authorization}
        response = requests.post(url, json=data, headers=headers)
        returned_data = json.loads(response.text)

@frappe.whitelist()
def receive_support_comment(**kwargs):
    user = frappe.session.user
    if user == "support@erpcloud.systems":
        comment = frappe.get_doc(kwargs)
        comment.save(ignore_permissions=True)
        comment_name = comment.name
        frappe.db.commit()
        if comment_name:
            return comment.name
        else:
            return "Comment Not Added"