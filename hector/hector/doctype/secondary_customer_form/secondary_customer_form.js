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
        var mobile_pattern = "^\\d{10,11}$";
        var email_pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"

        if(phone.length > 0  && !phone.match(mobile_pattern))
        {
            frappe.throw('Enter Valid Phone Number')
        }

        if(email.length > 0  && !email.match(email_pattern))
        {
            frappe.throw('Enter Valid Email ID')
        }



    }
});
