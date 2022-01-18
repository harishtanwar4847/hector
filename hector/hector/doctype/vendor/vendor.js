// Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor', {
    refresh: function(frm) {
		if(frm.doc.workflow_state == "Requested for Vendor Creation"){
		    frm.set_intro("Vendor Code is Mandatory for Approval");
		}

	}
});
