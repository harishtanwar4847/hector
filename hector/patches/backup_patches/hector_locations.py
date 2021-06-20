import frappe
from frappe.core.doctype.data_import.data_import import import_file
def execute():
    path = frappe.get_app_path('hector','patches','imports','hector_locations.csv')
    # file_path = '"'+path+
    import_file('Hector Locations', path, 'Insert', submit_after_import=True)