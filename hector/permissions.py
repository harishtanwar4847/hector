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
    if ('Area Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside ASM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "((`tabCustomer Form`.owner = '{user}') OR (`tabCustomer Form`.asm_user = '{user}'))".format(user=frappe.session.user)
    # #    return "(`tabCustomer Form`.workflow_state = 'Pending For NSM Approval')"

    if('Regional Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside RSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabCustomer Form`.rsm = '{user}')".format(user=frappe.session.user)
        return "((`tabCustomer Form`.owner in (SELECT `tabCustomer Form`.owner FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}')) OR (`tabCustomer Form`.asm_user in (SELECT `tabCustomer Form`.asm_user FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}')))".format(user=frappe.session.user)

    if('National Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside NSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabCustomer Form`.rsm = '{user}')".format(user=frappe.session.user)
        return "((`tabCustomer Form`.owner in (SELECT `tabCustomer Form`.owner FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}')) OR (`tabCustomer Form`.asm_user in (SELECT `tabCustomer Form`.asm_user FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.rsm_user OR `tabCustomer Form`.asm_user = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}')))".format(user=frappe.session.user)
        # return "(`tabCustomer Form`.owner in (SELECT `tabCustomer Form`.owner FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}'))".format(user=frappe.session.user)

    if('Primary Customer Master Approver' in frappe.get_roles(user) or 'Secondary Customer Master Approver' in frappe.get_roles(user) or 'Sales Manager' in frappe.get_roles(user) or 'Sales User' in frappe.get_roles(user) or 'System Manager' in frappe.get_roles(user) or 'Sales Master Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside CMA MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "(`tabCustomer Form`.docstatus = '0')"

def secondary_customer_form_query(user = frappe.session.user):
    if ('Area Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside ASM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "((`tabSecondary Customer Form`.owner = '{user}') OR (`tabSecondary Customer Form`.asm_user = '{user}'))".format(user=frappe.session.user)
    
    if('Regional Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside RSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabSecondary Customer Form`.rsm = '{user}')".format(user=frappe.session.user)
        return "((`tabSecondary Customer Form`.owner in (SELECT `tabSecondary Customer Form`.owner FROM `tabSecondary Customer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}')) OR (`tabSecondary Customer Form`.asm_user in (SELECT `tabSecondary Customer Form`.asm_user FROM `tabSecondary Customer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.so_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.ase_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.asm_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.rsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}')))".format(user=frappe.session.user)

    if('National Sales Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside NSM MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        # return "(`tabSecondary Customer Form`.rsm = '{user}')".format(user=frappe.session.user)
        return "((`tabSecondary Customer Form`.owner in (SELECT `tabSecondary Customer Form`.owner FROM `tabSecondary Customer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user OR `tabSecondary Customer Form`.owner = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}')) OR (`tabSecondary Customer Form`.asm_user in (SELECT `tabSecondary Customer Form`.asm_user FROM `tabSecondary Customer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.so_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.ase_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.asm_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.rsm_user OR `tabSecondary Customer Form`.asm_user = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}')))".format(user=frappe.session.user)
        # return "(`tabCustomer Form`.owner in (SELECT `tabCustomer Form`.owner FROM `tabCustomer Form` INNER JOIN `tabSales Hierarchy Mapping` ON `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.so_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.ase_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.asm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.rsm_user OR `tabCustomer Form`.owner = `tabSales Hierarchy Mapping`.nsm_user where `tabSales Hierarchy Mapping`.so_user = '{user}' OR `tabSales Hierarchy Mapping`.ase_user = '{user}' OR `tabSales Hierarchy Mapping`.asm_user = '{user}' OR `tabSales Hierarchy Mapping`.rsm_user = '{user}' OR `tabSales Hierarchy Mapping`.nsm_user = '{user}'))".format(user=frappe.session.user)

    if('Secondary Customer Master Approver' in frappe.get_roles(user) or 'Sales Manager' in frappe.get_roles(user) or 'Sales User' in frappe.get_roles(user) or 'System Manager' in frappe.get_roles(user) or 'Sales Master Manager' in frappe.get_roles(user)):
        print('\n\n\n<<<<<<<<<<<<Inside CMA MAPPING QUERY>>>>>>>>>>>>\n\n\n')
        return "(`tabSecondary Customer Form`.docstatus = '0')"

def quality_issue_query(user = frappe.session.user):
    # passs
    if ('Physical Verification Officer' in frappe.get_roles(user) and 'Administrator' not in frappe.get_roles(user)):
        print("\n\nInside Physical Verification Officer Query\n\n")
        return "(`tabQuality Issue`.physicalremote_verification_executive_email = '{}')".format(user)
    else :
        return "(`tabQuality Issue`.docstatus = '0')"
