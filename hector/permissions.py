import frappe

def customer_query(user = frappe.session.user):
    if('Regional Sales Manager' in frappe.get_roles(user)):
        # return "(`tabCustomer`.rsm = '{user}')".format(user=frappe.session.user)
        return "(`tabCustomer`.owner in (SELECT `tabCustomer`.owner FROM `tabCustomer` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}'))".format(user=frappe.session.user)

    if('Customer Master Approver' in frappe.get_roles(user)):
        return "(`tabCustomer`.naming_series = 'CUST-.YYYY.-')"