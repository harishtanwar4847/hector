import frappe

def customer_query(user):
    if not user:
        user = frappe.session.user
        has_roles = frappe.get_roles(user)
        if ('Customer Master Approver' not in has_roles)  or ('System Manager' not in has_roles):
            print(f'\n\n\n\n\n<<<<<<<<<<<<<<<<<<<{has_roles}>>>>>>>>>>>>>>>>>>>>>\n\n\n\n\n')
            # return "(`tabCustomer`.rsm = '{user}')".format(user=frappe.session.user)
            return "(`tabCustomer`.owner in (SELECT `tabCustomer`.owner FROM `tabCustomer` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}'))".format(user=frappe.session.user)
