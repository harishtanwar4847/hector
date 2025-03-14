# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TransitIssue(Document):
	def on_update(self):
		rsmEmail = self.rsm_name
		asmEmail = self.asm_name
		requestorSalesTeam = self.email_address_of_requestor_from_sales_team
		complaintTeamEmail = self.owner
		complaintTeamName = frappe.get_doc('User', complaintTeamEmail).full_name
		supplyTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Supply Team'""", as_list=1)]
		supplyTeamEmail.remove('Administrator')
		financeTeamEmail = [x[0] for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamEmail.remove('Administrator')
		financeTeamName = [x[0] for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamName.remove('Administrator')
		emailMessage = """You have been requested to review the following:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)

		if self.workflow_state == 'Rejected by Transit complaint Registration Team' :
			frappe.db.set_value('Transit Issue', self.name, 'transit_complaint_registration_team_rejection_time', frappe.utils.now())

		if self.workflow_state == 'Pending for Supply Team Approval' :
			frappe.db.set_value('Transit Issue', self.name, 'pending_supply_team_time', frappe.utils.now())
			#For sending approval email to Supply Team
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue Pending for Supply Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team of customer complaint registered
			message1 = """Below Transit Issue have been Registered:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Transit Issue registered: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal ,recipients = '{}'.format(requestorSalesTeam), cc = '{},{}'.format(rsmEmail, asmEmail),expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Supply Team Approval' :
			frappe.db.set_value('Transit Issue', self.name, 'resent_supply_team_time', frappe.utils.now())
			msg=emailMessage
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue Resent for Supply Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Supply Team' :
			frappe.db.set_value('Transit Issue', self.name, 'supply_team_rejection_time', frappe.utils.now())
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = msg + message2 + message3
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team and customer of Issue rejected process
			message1 = """Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Requested for More Details by Supply Team':
			frappe.db.set_value('Transit Issue', self.name, 'request_details_supply_team_time', frappe.utils.now())
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Finance Team':
			frappe.db.set_value('Transit Issue', self.name, 'request_details_finance_team_time', frappe.utils.now())
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue requesting for more details: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Finance Team':
			frappe.db.set_value('Transit Issue', self.name, 'finance_team_rejection_time', frappe.utils.now())
			msg="""Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue, self.reason_of_rejection)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = msg + message2 + message3
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sendng email to sales team and customer of Issue rejected process
			message1 = """Below Transit Issue have been Rejected:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """Comment: {}<br><br><br>
			Regards,<br>
			Hector Beverages""".format(self.reason_of_rejection)
			messageFinal = message1 + message2 + message3
			frappe.sendmail(subject="Transit Issue Rejected: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")


		if self.workflow_state == 'Pending for Finance Team Approval':
			frappe.db.set_value('Transit Issue', self.name, 'pending_finance_team_time', frappe.utils.now())
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue Pending for Finance Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = financeTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Finance Team Approval':
			frappe.db.set_value('Transit Issue', self.name, 'resent_finance_team_time', frappe.utils.now())
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue Resent for Finance Team Approval: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = financeTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Issue Closed':
			frappe.db.set_value('Transit Issue', self.name, 'finance_team_approval_time', frappe.utils.now())
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message3 = """<br><br><br>
			Regards,<br>
			Hector Beverages"""
			messageFinal = emailMessage + message2 + message3
			frappe.sendmail(subject="Transit Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			#For sendng email to sales team of credit note raised process
			message1 = """Below Transit Issue have been Closed:<br>
			<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
					<tr>
						<td>Ticket No:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Location:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{}</td>
					</tr>
				</tbody>
			</table><br>""".format(self.name, self.customer_name, self.customer_code, self.customer_location, self.customer_phone_number, self.type_of_issue)
			message2 = """<table border="1" cellspacing="0" cellpadding="5" align="">
			<tr><th>Invoice Number</th><th>SKU Code</th><th>SKU Name</th><th>Batch Details</th><th>Damaged /Missing Quantity</th></tr>
			"""
			for skuRow in self.sku_details:
				message2 += "<tr><td>" + skuRow.invoice_number + "</td><td>"+skuRow.sku_code + "</td><td>"+skuRow.sku_name + "</td><td>" + skuRow.batch_details + "</td><td>" + skuRow.damaged_missing_quantity + "</td><tr>"
			message2 += "</table><br>"
			message4 = """
				Credit Details: {}<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.credit_details)
			messageFinal = message1 + message2 + message4
			frappe.sendmail(subject="Transit Issue Completed: {}: {}".format(self.customer_code, self.customer_name), content=messageFinal, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == "Rejected and transferred as Quality Complaint" and (self.get_doc_before_save().workflow_state != self.workflow_state):
			print('inside code-------------------------------------')
			# set value of transferred_as_quality_ticket_time
			frappe.db.set_value('Transit Issue', self.name, 'transferred_as_quality_ticket_time', frappe.utils.now())
			
			# create a new quality issue
			doc = frappe.new_doc('Quality Issue')
			doc.asm_name = self.asm_name
			doc.rsm_name = self.rsm_name
			doc.customer_name = self.customer_name
			doc.customer_code = self.customer_code
			doc.customer_state = self.customer_state
			doc.email_address_of_requestor_from_sales_team = self.email_address_of_requestor_from_sales_team
			doc.customer_location = self.customer_location
			doc.customer_phone_number = self.customer_phone_number
			for i in self.sku_details:
				doc.append('sku_details', {
					'sku_code': i.sku_code,
					'sku_name': i.sku_name,
					'quantity_in_pieces': i.damaged_missing_quantity,
					'batch_details': i.batch_details
				})
			doc.complaint_reported_date = self.complaint_reported_date
			doc.reference_old_ticket_number = self.name
			doc.owner = self.owner
			doc.save(ignore_permissions=True)
