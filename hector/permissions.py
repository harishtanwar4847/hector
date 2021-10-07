import frappe

def customer_query(user = frappe.session.user):
    if('Regional Sales Manager' in frappe.get_roles(user) or 'Area Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside RSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabCustomer`.rsm = '{user}')".format(user=frappe.session.user)
        return "(`tabCustomer`.owner in (SELECT `tabCustomer`.owner FROM `tabCustomer` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}'))".format(user=frappe.session.user)

    if('Customer Master Approver' in frappe.get_roles(user) or 'Sales Manager' in frappe.get_roles(user) or 'Sales User' in frappe.get_roles(user) or 'System Manager' in frappe.get_roles(user) or 'Sales Master Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside CMA MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "(`tabCustomer`.naming_series = 'CUST-.YYYY.-')"

def customer_form_query(user = frappe.session.user):
    if ('Area Sales Manager' in frappe.get_roles(user) and not ('Regional Sales Manager' in frappe.get_roles(user) and 'Area Sales Manager' in frappe.get_roles(user))):
        print('\n\n\n<<<<<<<<<<<<Inside ASM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "(`tabCustomer Form`.owner = '{user}')".format(user=frappe.session.user)

    if('Regional Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside RSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabCustomer Form`.rsm = '{user}')".format(user=frappe.session.user)
        return "(`tabCustomer Form`.owner in (SELECT `tabCustomer Form`.owner FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}'))".format(user=frappe.session.user)

    if('Customer Master Approver' in frappe.get_roles(user) or 'Sales Manager' in frappe.get_roles(user) or 'Sales User' in frappe.get_roles(user) or 'System Manager' in frappe.get_roles(user) or 'Sales Master Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside CMA MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "(`tabCustomer Form`.docstatus = '0')"

def quality_issue_query(user = frappe.session.user):
    # passs
    if ('Physical Verification Officer' in frappe.get_roles(user) and 'Administrator' not in frappe.get_roles(user)):
        print("\n\nInside Physical Verification Officer Query\n\n")
        return "(`tabQuality Issue`.physicalremote_verification_executive_email = '{}')".format(user)
    else :
        return "(`tabQuality Issue`.docstatus = '0')"
