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
    let pan_pattern = /[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
    var phone = frm.doc.phone || ""
    var pin = frm.doc.pincode || ""
    var experience = frm.doc.enter_distribution_experience_in_years || ""
    var average_salary =  frm.doc.monthly_turn_over || ""
    var vehicles = frm.doc.number_of_vehicles_for_distribution || ""
    var infra = frm.doc.infrastructure || ""
    let pan_number = frm.doc.pan_number || ""
    var number_list = ['0','1','2','3','4','5','6','7','8','9']

    if(phone.length > 0  && !phone.match(mobile_pattern))
        {
            frappe.throw('Enter Valid Phone Number')
        }
    if(pin.length>0 && !pin.match(pin_pattern))
        {
            frappe.throw('Enter Valid Pin Code')
        }
    if (experience.length == 1){
      if(!(number_list.includes(experience[0])))
	        {
	            frappe.throw('Enter Valid distribution experience in years')
	        }   
    }
    if (experience.length == 2){
      if(!(number_list.includes(experience[0]) && number_list.includes(experience[1])))
	        {
	            frappe.throw('Enter Valid distribution experience in years')
	        }   
    }
    if (experience.length == 3){
      if(!(number_list.includes(experience[0]) && number_list.includes(experience[1]) && number_list.includes(experience[2])))
	        {
	            frappe.throw('Enter Valid distribution experience in years')
	        }   
    }
    if (experience.length>3)
        {
            frappe.throw('Distribution experience in years can be a maximum 3 digit number')
        }

    if(average_salary > 9999){
        frappe.throw('Average monthly sales in lakhs can be a maximum 4 digit number')
    }
    if(vehicles > 999){
      frappe.throw('Number of vehicles for distribution can be a maximum 3 digit number')
  }
    if(infra > 99999999999999999999){
      frappe.throw('Infrastructure(In Sq. ft) can be a maximum 20 digit number')
    }
    
    if (pan_number.length > 0 && !pan_number.match(pan_pattern)) {
      frappe.throw(__('Invalid PAN Number'));
    }
    
  }

  
})