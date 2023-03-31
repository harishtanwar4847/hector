import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('hector','patches','imports5','workflow_state.csv')
    import_file('Workflow State', path, 'Insert',console=True)
    path = frappe.get_app_path('hector','patches','imports5','workflow.csv')
    import_file('Workflow', path, 'Insert',console=True)