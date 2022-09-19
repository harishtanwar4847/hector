frappe.listview_settings['Lead'] = {
    onload(listview) {
        var route_options = {}
        console.log(listview)
        if(frappe.user_roles.includes('Customer Support Team'))
        {
            route_options = {
				"workflow_state": ["in",'Pending with Customer Support Team']
			};
        }
        frappe.route_options = route_options;
    }
};