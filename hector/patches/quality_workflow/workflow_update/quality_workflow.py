import frappe
from frappe.core.doctype.data_import.data_import import import_file

def execute():
    path = frappe.get_app_path('hector','patches','quality_workflow','imports','workflow_state.csv')
    import_file('Workflow State', path, 'Update',console=True)
    path = frappe.get_app_path('hector','patches','quality_workflow','imports','workflow_action_master.csv')
    import_file('Workflow Action Master', path, 'Update',console=True)
    path = frappe.get_app_path('hector','patches','quality_workflow','imports','quality_workflow.csv')
    import_file('Workflow', path, 'Update',console=True)
