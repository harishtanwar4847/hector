import frappe
from frappe.core.doctype.data_import.data_import import import_file
def execute():
    path = frappe.get_app_path('hector','patches','imports','workflow_state.csv')
    import_file('Workflow State', path, 'Insert')