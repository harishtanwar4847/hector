frappe.listview_settings['Secondary Customer Form'] = {
    onload(listview) {
        var route_options = {}
        console.log(listview)
        if(frappe.user_roles.includes('Regional Sales Manager') && frappe.user_roles.includes('Area Sales Manager'))
        {
            route_options = {
				"workflow_state": ["not in", 'Secondary Customer Approved']
			};
        }
        if(frappe.user_roles.includes('Area Sales Manager') || frappe.user_roles.includes('Regional Sales Manager'))
        {
            route_options = {
				"workflow_state": ["in",'Pending For Secondary Customer Additional Details, Requested for More Details by NSM, Requested for More Details by Secondary Master Team'],
				// "workflow_state": ["=",'Requested for More Details by Master Team']
			};
        }
        if(frappe.user_roles.includes('National Sales Manager'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for NSM Approval,Resent for NSM Approval']
			};
        }
        if(frappe.user_roles.includes('RTM Manager'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for RTM Approval,Resent for RTM Approval']
			};
        }
        if(frappe.user_roles.includes('Secondary Customer Master Approver'))
        {
            route_options = {
				"workflow_state": ["in",'Resent for Secondary Master Processing, Pending with Secondary Master Processing']
			};
        }
        frappe.route_options = route_options
        // frappe.db.get_list('Customer', {
        //     fields: ['customer_name','asm','rsm'],
        //     filters: {
        //         rsm : frappe.session.user
        //     }
        // }).then(records => {
        //     console.log(records);
        //     return records;
        // })
	},
	before_render(){

	}
}
