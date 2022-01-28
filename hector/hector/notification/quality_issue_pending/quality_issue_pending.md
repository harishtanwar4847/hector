Hello Sir,<br><br>
This is to inform you that there has been a Quality/Transit Complaint ticket placed. Please Find ticket details below:
<table>
				<tbody>
                    <tr>
						<td>Ticket No.:</td>
						<td>{{doc.name}}</td>
					</tr>
					<tr>
						<td>Customer Name:</td>
						<td>{{doc.customer_name}}</td>
					</tr>
					<tr>
						<td>Customer Code:</td>
						<td>{{doc.customer_code}}</td>
					</tr>
					<tr>
						<td>Customer Loocation:</td>
						<td>{{doc.customer_location}}</td>
					</tr>
					<tr>
						<td>Customer Phone Number:</td>
						<td>{{doc.customer_phone_number}}</td>
					</tr>
					<tr>
						<td>Type of Issue:</td>
						<td>{{doc.type_of_issue}}</td>
					</tr>
					<tr>
						<td>Invoice Number:</td>
						<td>{{doc.invoice_number}}</td>
					</tr>
					<tr>
						<td>ASM:</td>
						<td>{% set var = frappe.db.get_value("User", doc.asm_name, "full_name") %} {{var}}</td>
					</tr>
					<tr>
						<td>RSM:</td>
						<td>{% set var = frappe.db.get_value("User", doc.rsm_name, "full_name") %} {{var}}</td>
					</tr>
					<tr>
						<td>Total SKU(in Pieces):</td>
						<td>{% for row in doc.sku_details %} {{row.quantity_in_pieces}} {% endfor %}</td>
					</tr>
				</tbody>
			</table><br><br>
			Regards,<br>
			Hector Beverages
