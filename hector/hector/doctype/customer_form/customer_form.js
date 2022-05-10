frappe.ui.form.on('Customer Form', {
    onload(frm){
        if(frm.doc.workflow_state == "Primary Customer Approved" || frm.doc.workflow_state == "Secondary Customer Approved")
	    {
	        frm.page.sidebar.remove();
	    }
    },
	refresh(frm){
        if (frm.is_new() && (frappe.user_roles.includes("Area Sales Manager") || frappe.user_roles.includes("Regional Sales Manager"))){
            frm.set_value("asm_user", frappe.session.user)
        }
        if(frm.doc.workflow_state == 'Pending for TOT Approval from Customer')
	    {
	        frm.set_intro('Please Attach TOT Acceptance Email');
	    }
	    if(frm.doc.workflow_state == 'Pending with Primary Master Processing' || frm.doc.workflow_state == 'Resent for Primary Master Processing')
	    {
	        frm.set_intro('Please Enter Customer ID');
	    }
	},
	before_load(frm){
	},
	validate(frm){

	    function isEmpty(val){
            return (val === undefined || val == null || val.length <= 0) ? true : false;
        }
	    var number_list = ['0','1','2','3','4','5','6','7','8','9']
	    var char_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	    var gstin = frm.doc.gst_registration_number
	    if (frm.doc.customer_type === "Super Stockist" || !isEmpty(gstin)) {
	    if(gstin.length == 15)
	    {
	       // console.log(gstin)
	        if(!(number_list.includes(gstin[0]) && number_list.includes(gstin[1]) && char_list.includes(gstin[2]) && char_list.includes(gstin[3]) && char_list.includes(gstin[4])
	         && char_list.includes(gstin[5]) && char_list.includes(gstin[6]) && number_list.includes(gstin[7]) && number_list.includes(gstin[8])
	          && number_list.includes(gstin[9]) && number_list.includes(gstin[10]) && char_list.includes(gstin[11]) && number_list.includes(gstin[12])
	           && char_list.includes(gstin[13]) && (number_list.includes(gstin[14]) || char_list.includes(gstin[14]))))
	        {
	            frappe.throw('Enter Valid GST Number.')
	        }
        }
        else
        {
            frappe.throw('Enter Valid GST Number.')
        }
	    }
        var pan = frm.doc.pan_card_no
        if(pan.length == 10)
	    {
	        console.log(gstin)
	        if(!(char_list.includes(pan[0]) && char_list.includes(pan[1]) && char_list.includes(pan[2]) && char_list.includes(pan[3]) && char_list.includes(pan[4])
	         && number_list.includes(pan[5]) && number_list.includes(pan[6]) && number_list.includes(pan[7]) && number_list.includes(pan[8])
	          && char_list.includes(pan[9])))
	        {
	            frappe.throw('Enter Valid Pan Card Number.')
	        }
        }
        else
        {
            frappe.throw('Enter Valid PAN Card Number.')
        }
        var ph_number = frm.doc.mobile_no_of_the_customer
        if(ph_number.length == 10)
        {
            if(!(number_list.includes(ph_number[0]) && number_list.includes(ph_number[1]) && number_list.includes(ph_number[2]) && number_list.includes(ph_number[3])
	          && number_list.includes(ph_number[4]) && number_list.includes(ph_number[5]) && number_list.includes(ph_number[6]) && number_list.includes(ph_number[7])
	          && number_list.includes(ph_number[8]) && number_list.includes(ph_number[9])))
	        {
	            frm.doc.mobile_no_of_the_customer = ''
	            frm.refresh_field('mobile_no_of_the_customer');
	            frappe.throw('Enter Valid Mobile Number.')
	        }
        }
        else
        {
            frm.doc.mobile_no_of_the_customer = ''
	        frm.refresh_field('mobile_no_of_the_customer');
            frappe.throw('Enter Valid Mobile Number.')
        }
        var post_code = frm.doc.post_code;
        if(post_code.length == 6)
        {
            if(!(number_list.includes(post_code[0]) && number_list.includes(post_code[1]) && number_list.includes(post_code[2]) && number_list.includes(post_code[3])
	          && number_list.includes(post_code[4]) && number_list.includes(post_code[5])))
	        {
	            frm.doc.post_code = ''
	            frm.refresh_field('post_code');
	            frappe.throw('Enter Valid Post Code.')
	        }
        }
        else
        {
            frm.doc.post_code = ''
            frm.refresh_field('post_code');
	        frappe.throw('Enter Valid Post Code.')
        }
        var post_code_ship = frm.doc.post_code_for_shipping_address;
        if(post_code_ship.length == 6)
        {
            if(!(number_list.includes(post_code_ship[0]) && number_list.includes(post_code_ship[1]) && number_list.includes(post_code_ship[2])
            && number_list.includes(post_code_ship[3]) && number_list.includes(post_code_ship[4]) && number_list.includes(post_code_ship[5])))
	        {
	            frm.doc.post_code_for_shipping_address = ''
	            frm.refresh_field('post_code_for_shipping_address');
	            frappe.throw('Enter Valid Shipping Address Post Code.')
	        }
        }
        else
        {
            frm.doc.post_code_for_shipping_address = ''
            frm.refresh_field('post_code_for_shipping_address');
	        frappe.throw('Enter Valid Shipping Address Post Code.')
        }
        if(!(frm.doc.customer_email_address.includes('@') && frm.doc.customer_email_address.toLowerCase().includes('.com' || '.org' || '.in')))
        {
            frappe.throw('Enter Valid Email.')
            frm.doc.customer_email_address = ''
        }
        if(frm.doc.workflow_state == "Pending for Master Team Approval")
        {
            if(frm.doc.customer_id[0] != "C")
            {
                frappe.throw('Customer ID should began with C.');
            }
        }
	}
})
