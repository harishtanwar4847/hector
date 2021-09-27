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
		financeTeamEmail = [x for x in frappe.db.sql("""select u.name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamEmail.remove(['Administrator'])
		financeTeamEmail = financeTeamEmail[0][0]
		financeTeamName = [x for x in frappe.db.sql("""select u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Finance Team'""", as_list=1)]
		financeTeamName.remove(['Administrator'])
		financeTeamName = financeTeamName[0][0]


		if self.workflow_state == 'Pending for Supply Team Approval' :
			#For sendng email to sales team of customer complaint registered
			msg="""Hello {},<br><br>
				Your Complaint has been registered.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Complaint Registered", content=msg,recipients = '{}'.format(requestorSalesTeam), cc = '{},{}'.format(rsmEmail, asmEmail),expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")
			#For sending approval email to Supply Team
			msg="""Hello Team,<br><br>
			You have received a request for transit complaint from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Pending for Supply Team Approval", content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Supply Team Approval' :
			msg="""Hello Team,<br><br>
			You have received a request for transit complaint from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Resent for Supply Team Approval", content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Supply Team' :
			msg="""Hello {},<br><br>
			You have received a request is rejected by Supply Team for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Rejected by Supply Team", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Supply Team':
			msg="""Hello {},<br><br>
			You have received a request for more details from Supply Team for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Requested for More Details by Supply Team", content=msg, recipients = '{}'.format(complaintTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Requested for More Details by Finance Team':
			msg="""Hello {},<br><br>
			You have received a request for more details from {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(complaintTeamName,financeTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Requested for More Details by Finance Team", content=msg, recipients = supplyTeamEmail,sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Rejected by Finance Team':
			msg="""Hello Team,<br><br>
			Your request for quality team approval is rejected by {} for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Rejected by Finance Team", content=msg, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Pending for Finance Team Approval':
			msg="""Hello {},<br><br>
			You have received a request for finance team approval from Supply Team for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Pending for Finance Team Approval", content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Resent for Finance Team Approval':
			msg="""Hello {},<br><br>
			You have received a request for finance team approval from Supply Team for the customer {}.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Resent for Finance Team Approval", content=msg, recipients = '{}'.format(financeTeamEmail),sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

		if self.workflow_state == 'Issue Closed':
			msg="""Hello Team,<br><br>
			Your request for Transit Complaint for the customer {} is Closed.<br><br>
			Kindly login to apps.myhector.com for the approval process.<br><br><br>
			Regards,<br>
			Hector Beverages""".format(financeTeamName, self.customer_name)
			frappe.sendmail(subject="Transit Complaints: Issue Closed", content=msg, recipients = [complaintTeamEmail] + supplyTeamEmail, sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

			#For sendng email to sales team of credit note raised process
			msg="""Hello Team,<br><br>
				Credit Note raised for the customer {}.<br><br>
				Kindly login to apps.myhector.com for the approval process.<br><br><br>
				Regards,<br>
				Hector Beverages""".format(self.customer_name)
			frappe.sendmail(subject="Customer Complaints: Credit Note Raised", content=msg, cc = '{},{}'.format(rsmEmail, asmEmail), recipients = '{}'.format(requestorSalesTeam), expose_recipients="header", sender="Notification@hectorbeverages.com")
			print("\n email sent \n")

