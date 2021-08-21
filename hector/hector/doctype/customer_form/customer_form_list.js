frappe.listview_settings['Customer Form'] = {
    onload(listview) {
        var route_options = {}
        console.log(listview)
        if(frappe.user_roles.includes('Regional Sales Manager') && frappe.user_roles.includes('Area Sales Manager'))
        {
            route_options = {
				"workflow_state": ["!=",'Customer Approved']
			};
        }
        if(frappe.user_roles.includes('Area Sales Manager'))
        {
            route_options = {
				"workflow_state": ["in",'Requested for More Details by RSM, Requested for More Details by Master Team'],
				// "workflow_state": ["=",'Requested for More Details by Master Team']
			};
        }
        if(frappe.user_roles.includes('Regional Sales Manager'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for RSM Approval,Resent for RSM Approval &nbsp;']
			};
        }
        if(frappe.user_roles.includes('Customer Master Approver'))
        {
            route_options = {
				"workflow_state": ["in",'Resent for Master Team Approval &nbsp;,Pending for TOT Approval from Customer,Pending for Master Team Approval']
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
