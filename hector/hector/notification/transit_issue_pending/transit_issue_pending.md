Hello Sir,<br><br>
This is to inform you that there has been a Transit Complaint ticket placed. Please Find ticket details below:
<table border="1" cellspacing="0" cellpadding="5" align="">
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
						<td>{% for row in doc.sku_details %} {{row.invoice_number}} {% endfor %}</td>
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
						<td>{% set var = namespace (qty = 0) %}{% for item in doc.sku_details %}{% set list1 = item.damaged_missing_quantity.split(' ') %}{% set var.qty = var.qty + list1[0]|int %}{% endfor %} {{ var.qty }}</td>


					</tr>
				</tbody>
			</table><br><br>
<table border="1" cellspacing="0" cellpadding="5" align="">
				<tbody>
                    <tr>
                        <td>Invoice Number</td>
						<td>SKU Code</td>
						<td>SKU Name</td>
						<td>Batch details</td>
						<td>Damaged/Missing Quantity</td>
					</tr>
					{% for item in doc.sku_details %}
					<tr>
					    <td>{{item.invoice_number}}</td>
						<td>{{item.sku_code}}</td>
						<td>{{item.sku_name}}</td>
						<td>{{item.batch_details}}</td>
						<td>{{item.damaged_missing_quantity}}</td>
					</tr>
					{% endfor %}
				</tbody>
			</table><br><br>
			Regards,<br>
			Hector Beverages