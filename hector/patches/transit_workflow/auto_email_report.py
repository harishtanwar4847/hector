import frappe
from frappe.core.doctype.data_import.data_import import import_file
def execute():
    path = frappe.get_app_path('hector','patches','transit_workflow','imports','auto_email_report.csv')
    import_file('Auto Email Report', path, 'Insert')
