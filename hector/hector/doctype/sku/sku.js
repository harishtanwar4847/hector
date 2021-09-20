frappe.ui.form.on('SKU', {
	refresh(frm) {
		// your code here
	},
	validate(frm){
	    if (isNaN(frm.doc.nav_sku_code))
	    {
	        frappe.throw("Nav SKU Code should be a Number")
	    }
	    if (isNaN(frm.doc.sku_variant_code))
	    {
	        frappe.throw("SKU Variant Code should be a Number")
	    }
	    if (isNaN(frm.doc.sku_mrp))
	    {
	        frappe.throw("SKU MRP should be a Number")
	    }
	}
})
