# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import frappe.desk.desktop
__version__ = '1.5.8-dev'


# def get_page_for_user(self):
#   roles_list = frappe.get_all("Has Role",filters={'parent':frappe.session.user},fields=['role'])
#   print(f'\n\n\n\n\n\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{roles_list}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n\n\n\n\n')
#   # filters = {
#   #   'extends': self.page_name,
#   #   'for_user': frappe.session.user
#   # }
#   # user_pages = frappe.get_all("Workspace", filters=filters, limit=1)
#   for role in roles_list:

#     if (role.role == "Area Sales Manager" and role.role == "Regional Sales Manager") or (role.role == "Regional Sales Manager"):
#         return frappe.get_doc("Workspace", "RSM Workspace")

#     if role.role == "Area Sales Manager":
#         return frappe.get_doc("Workspace", "ASM Workspace")

#     if role.role == "Customer Master Approver":
#         return frappe.get_doc("Workspace", "CMA Workspace")

#     else:
#         return frappe.get_doc("Workspace", "Home")

#   filters = {
#     'extends_another_page': 1,
#     'extends': self.page_name,
#     'is_default': 1
#   }
#   default_page = frappe.get_all("Workspace", filters=filters, limit=1)
#   if default_page:
#     return frappe.get_cached_doc("Workspace", default_page[0])

#   self.get_pages_to_extend()
#   return frappe.get_cached_doc("Workspace", self.page_name)

# frappe.desk.desktop.Workspace.get_page_for_user = get_page_for_user
