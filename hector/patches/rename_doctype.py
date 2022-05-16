from __future__ import unicode_literals
import frappe
from frappe.core.doctype.data_import.data_import import import_file
from frappe.modules.import_file import import_file_by_path

def execute():
    doc_path1 = frappe.get_app_path('hector', 'hector', 'doctype', 'primary_customer_form', 'primary_customer_form.json')
    import_file_by_path(doc_path1, force=True, ignore_version=True, reset_permissions=True, for_sync=True)
    doc_path2 = frappe.get_app_path('hector', 'hector', 'doctype', 'secondary_customer_form', 'secondary_customer_form.json')
    import_file_by_path(doc_path2, force=True, ignore_version=True, reset_permissions=True, for_sync=True)
