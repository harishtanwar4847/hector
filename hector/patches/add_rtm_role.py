from __future__ import unicode_literals
import frappe


def execute():
    if not frappe.db.exists("Role", "RTM Manager"):
        doc = frappe.new_doc("Role")
        doc.role_name = "RTM Manager"
        doc.insert()
        frappe.db.commit()