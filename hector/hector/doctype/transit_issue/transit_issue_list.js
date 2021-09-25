frappe.listview_settings['Transit Issue'] = {
    onload(listview) {
        var route_options = {}
        // console.log(listview)
        if(frappe.user_roles.includes('Complaint Registering Team'))
        {
            route_options = {
				"workflow_state": ["=",'Requested for More Details by Supply Team']
			};
        }
        if(frappe.user_roles.includes('Supply Team'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for Supply Team Approval,Resent for Supply Team Approval,Requested for More Details by Finance Team']
			};
        }
        if(frappe.user_roles.includes('Finance Team'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for Finance Team Approval,Resent for Finance Team Approval']
			};
        }
        if(frappe.user_roles.includes('System Manager') || frappe.user_roles.includes('Administrator'))
        {
            route_options = {}
        }
        frappe.route_options = route_options;
    }
}
