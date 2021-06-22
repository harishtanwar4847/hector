import frappe
from frappe.permissions import add_permission,update_permission_property

def execute():
    doctype_list = ['File','Workflow','Workflow State']
    for doctype in doctype_list:
        add_permission(doctype, 'CFA/Warehouse Manager')
    add_permission('File', 'CFA/Warehouse Manager', permlevel=1)
    file_doc_perm_zero = ['create','delete','email','export','import','print','read','report','select','set_user_permissions','share','write']
    for value in file_doc_perm_zero:
        update_permission_property('File', 'CFA/Warehouse Manager', 0, value,1)
    update_permission_property('File', 'CFA/Warehouse Manager', 1, 'write',1)

    frappe.db.commit()