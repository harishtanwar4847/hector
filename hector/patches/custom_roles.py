from __future__ import unicode_literals
import frappe


def execute():
    role_list = [
        "Area Sales Manager",
        "Regional Sales Manager",
        "Customer Master Approver",
    ]
    for role in role_list:
        if frappe.db.exists("Role", role) != role:
            doc = frappe.new_doc("Role")
            doc.role_name = role
            doc.insert()

    frappe.db.commit()
