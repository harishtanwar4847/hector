import frappe

def on_update(doc,method):
    if doc.workflow_state == "Primary Customer Created":
        res = frappe.new_doc("Customer Form")
        res.customer_name = doc.lead_name
        res.post_code = doc.pincode
        res.shipping_address = doc.address
        res.mobile_no_of_the_customer = doc.phone
        res.companies_presently_under_distribution = doc.brand_your_working_with
        res.total_turnover_of_the_firm = doc.monthly_turn_over
        res.gst_registration_number = doc.gst_number
        res.number_of_vehicles_assigned_for_delivery_ = doc.number_of_vehicles_for_distribution
        res.customer_type = doc.customer_type
        res.asm_user = doc.asm_user
        res.rsm_user = doc.rsm_user
        res.insert()
        frappe.msgprint("Primary Customer Created")
    
    if doc.workflow_state == "Secondary Customer Created":
        res2 = frappe.new_doc("Secondary Customer Form")
        res2.customer_type = doc.customer_type
        res2.asm_user = doc.asm_user
        res2.rsm_user = doc.rsm_user
        res2.name_of_new_distributor = doc.lead_name
        res2.distributor_contact_number = doc.phone
        res2.state = doc.state
        res2.distributor_district_name = doc.district
        res2.name_of_db_town = doc.city
        res2.other_company_brandhandled = doc.brand_your_working_with
        res2.total_turn_over_the_distributor_in_lakhs_in_a_month = doc.monthly_turn_over
        res2.no_of_outlets_covered = doc.total_outlets_handling
        res2.distributor_gst_no = doc.gst_number
        res2.number_of_vehicles = doc.number_of_vehicles_for_distribution
        res2.no_of_salesman = doc.sales_man_that_are_not_sponsor_by_other_brands
        res2.insert()
        frappe.msgprint("Secondary Customer Created")



