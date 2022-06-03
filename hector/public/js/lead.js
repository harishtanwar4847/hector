frappe.ui.form.on('Lead', {
	refresh: function(frm) {
    if ((frm.doc.workflow_state == "Pending with Customer Support Team" && !frm.doc.customer_type && !frm.is_new()) || (frm.doc.workflow_state == "Pending with Customer Support Team" && !frm.doc.asm_user && !frm.is_new())){
      frm.set_intro("Please Enter Type of Customer, ASM and RSM")
    }
  },
  validate(frm){
    var mobile_pattern = "^\\d{10,11}$";
    var pin_pattern = "^[1-9][0-9]{5}$"
    var gst_pattern = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$";
    var phone = frm.doc.phone || ""
    var pin = frm.doc.pincode || ""

    if(phone.length > 0  && !phone.match(mobile_pattern))
        {
            frappe.throw('Enter Valid Mobile Number')
        }
    if(pin.length>0 && !pin.match(pin_pattern))
        {
            frappe.throw('Enter Valid Pin Code')
        }
    
  }

  
})