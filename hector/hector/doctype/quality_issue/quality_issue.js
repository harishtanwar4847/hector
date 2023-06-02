frappe.ui.form.on('Quality Issue', {
	refresh(frm) {
		// your code here
		if(frm.doc.workflow_state == 'Pending for RCA Details')
	    {
	        frm.set_intro('Please Attach RCA Details');
	    }
        if((frm.doc.workflow_state == 'Pending for Finance Team Approval' || frm.doc.workflow_state == 'Resent for Finance Team Approval') && frappe.user_roles.includes('Finance Team'))
	    {
	        frm.set_intro('Please Enter Credit Details');
	    }
        if(frm.doc.workflow_state == 'Pending for confirmation with the Quality Complaint Registration Team' && (frm.doc.reference_old_ticket_number && !frm.doc.type_of_issue)){
            frm.set_intro(`This ticket has been transferred from Transit Issue. Please fill mandatory fields to proceed`)
        }
	},

    setup: function(frm) {
        frm.set_query('sku_code', 'sku_details', () => {
            return {
                filters: {
                    sku_inactive: 0
                }
            }
        })
    },

	validate(frm){

	    var number_pattern = /^\d{10}$/
	    var phone_number = frm.doc.customer_phone_number
        if (phone_number && !phone_number.match(number_pattern))
        {
            frappe.throw("Enter a valid Phone Number")
        }

        var email_address = frm.doc.email_address_of_requestor_from_sales_team
        var email_pattern =  /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/;
        if (email_address && !email_address.match(email_pattern))
        {
            frappe.throw('Enter Valid Email Address.')
        }

        var customer_code = frm.doc.customer_code
        if (customer_code && customer_code[0] !== "C")
        {
            frappe.throw('Customer Code should began with C.');
        }
        if(!frm.doc.___islocal || !frm.doc.reference_old_ticket_number) {
            frm.doc.sku_details.forEach(function(row) {
                // Check if the field in the child table row is empty
                if (!row.mgf_date) {
                    frappe.msgprint({
                        message: 'Manufacturing date in SKU Details is required',
                        indicator: 'red'
                    });
                    frappe.validated = false;
                }
            });
        }
	}
})
