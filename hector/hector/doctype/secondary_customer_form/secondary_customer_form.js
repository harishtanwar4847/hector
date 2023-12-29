// Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Secondary Customer Form', {
	refresh: function(frm) {
        if (frm.is_new() && (frappe.user_roles.includes("Area Sales Manager"))){
            frm.set_value("asm_user", frappe.session.user)
        }
        if (frm.is_new() && (frappe.user_roles.includes("Regional Sales Manager"))){
            frm.set_value("rsm_user", frappe.session.user)
        }
        if(frm.doc.workflow_state == 'Pending with Secondary Master Processing' || frm.doc.workflow_state == 'Resent for Secondary Master Processing')
	    {
	        frm.set_intro('Please Enter DB Code');
	    }
	},

    validate(frm){
        var phone = frm.doc.distributor_contact_number || ""
        var email = frm.doc.distributor_email_id || ""
        var town_code = frm.doc.please_enter_the_db_townunique_code_as_per_census_data || ""
        var town_code_1 = frm.doc.additional_town_1_code_as_per_census_file || ""
        var town_code_2 = frm.doc.additional_town_2_code_as_per_census_file || ""
        var town_code_3 = frm.doc.additional_town_3_code_as_per_census_file || ""
        var town_code_4 = frm.doc.additional_town_4_code_as_per_census_file || ""
        var town_code_5 = frm.doc.additional_town_5_code_as_per_census_file || ""
        var town_code_6 = frm.doc.additional_town_6_code_as_per_census_file || ""
        var town_code_7 = frm.doc.additional_town_7_code_as_per_census_file || ""
        var town_code_8 = frm.doc.additional_town_8_code_as_per_census_file || ""
        var town_code_9 = frm.doc.additional_town_9_code_as_per_census_file || ""
        var town_code_10 = frm.doc.additional_town_10_code_as_per_census_file || ""
        var mobile_pattern = "^\\d{10,11}$";
        var email_pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
        var town_code_pattern = "^\\d{6}$";

        if(phone.length > 0  && !phone.match(mobile_pattern))
        {
            frappe.throw('Enter Valid Phone Number')
        }

        if(email.length > 0  && !email.match(email_pattern))
        {
            frappe.throw('Enter Valid Email ID')
        }

        if (town_code.length > 0  && !town_code.match(town_code_pattern) && frm.doc.__islocal == 1){
            frappe.throw('Old Census codes are invalid, kindly enter the new 6 digits census code.')
        }

        if((town_code_1.length > 0  && !town_code_1.match(town_code_pattern)) || (town_code_2.length > 0  && !town_code_2.match(town_code_pattern)) || (town_code_3.length > 0  && !town_code_3.match(town_code_pattern)) || (town_code_4.length > 0  && !town_code_4.match(town_code_pattern)) || (town_code_5.length > 0  && !town_code_5.match(town_code_pattern)) || (town_code_6.length > 0  && !town_code_6.match(town_code_pattern)) || (town_code_7.length > 0  && !town_code_7.match(town_code_pattern)) || (town_code_8.length > 0  && !town_code_8.match(town_code_pattern)) || (town_code_9.length > 0  && !town_code_9.match(town_code_pattern)) || (town_code_10.length > 0  && !town_code_10.match(town_code_pattern)))
        {
            frappe.throw('Old Census codes are invalid, kindly enter the new 6 digits census code.')
        }

    }
});
