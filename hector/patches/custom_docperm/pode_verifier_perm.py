import frappe
from frappe.permissions import add_permission,update_permission_property

def execute():
    doctype_list = ['File','Data Export','Workflow State','Report']
    for doctype in doctype_list:
        add_permission(doctype, 'PODE Verifier')
    add_permission('File','PODE Verifier',permlevel=1)
    report_perm_zero = ['create','email','import','print','report','select','set_user_permissions','share','write']
    file_perm_zero = ['create','write']
    for value in report_perm_zero:
        update_permission_property('Report', 'PODE Verifier', 0, value,1)
    for value in file_perm_zero:
        update_permission_property('File', 'PODE Verifier', 0, value,1)
    update_permission_property('File', 'PODE Verifier', 1, 'write',1)
    frappe.db.commit()