// Copyright (c) 2022, Atrina Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Secondary Customer Form', {
	refresh: function(frm) {
        if (frm.is_new() && (frappe.user_roles.includes("Area Sales Manager") || frappe.user_roles.includes("Regional Sales Manager"))){
            frm.set_value("asm_user", frappe.session.user)
        }
	}
});
