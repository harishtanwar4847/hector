frappe.listview_settings['Quality Issue'] = {
    onload(listview) {
        var route_options = {}
        // console.log(listview)
        if(frappe.user_roles.includes('Complaint Registering Team'))
        {
            route_options = {
				"workflow_state": ["in",'Requested for More Details by Physical Verification Officer,Pending for confirmation with the Quality Complaint Registration Team,Rejected by Quality Complaint Registration Team']
			};
        }
        if(frappe.user_roles.includes('Physical Verification Officer'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for Physical Verification Officer Approval,Resent for Physical Verification Officer Approval,Requested for More Details by Finance Team,Pending for RCA Details,Requested for More Details by Quality Head']
			};
        }
        if(frappe.user_roles.includes('Finance Team'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for Finance Team Approval,Resent for Finance Team Approval']
			};
        }
        if(frappe.user_roles.includes('Quality Head'))
        {
            route_options = {
				"workflow_state": ["in",'Pending for Quality Head Approval,Resent for Quality Head Approval']
			};
        }
        if(frappe.user_roles.includes('System Manager') || frappe.user_roles.includes('Administrator'))
        {
            route_options = {}
        }
        frappe.route_options = route_options;
    }
}
