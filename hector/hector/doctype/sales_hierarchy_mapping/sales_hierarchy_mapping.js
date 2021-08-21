frappe.ui.form.on('Sales Hierarchy Mapping', {
	refresh(frm) {
		// your code here
	},
	before_save(frm){
	    frm.set_value('so_name', (frm.doc.so_user) ? frm.doc.so_name : '' );
	    frm.set_value('ase_name', (frm.doc.ase_user) ? frm.doc.ase_name : '' );
	    frm.set_value('asm_name', (frm.doc.asm_user) ? frm.doc.asm_name : '' );
	    frm.set_value('rsm_name', (frm.doc.rsm_user) ? frm.doc.rsm_name : '' );
	}
})
