import frappe
from frappe.permissions import add_permission,update_permission_property

def execute():
    doctype_list = ['File','Data Import','Workflow State']
    for doctype in doctype_list:
        add_permission(doctype, 'Invoice Importer')
    data_import_perm_zero = ['create','email','import','print','report','select','set_user_permissions','share','write']
    for value in data_import_perm_zero:
        update_permission_property('Data Import', 'Invoice Importer', 0, value,1)
    
    frappe.db.commit()