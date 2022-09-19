import click
import frappe

def execute():
    site_name = frappe.utils.get_site_base_path().replace("./", "")
    inp = click.prompt('Which site is this', type=click.Choice(['Dev', 'QA', 'UAT', 'Prod']))
    frappe.commands.popen("bench --site {} set-config server_type {}".format(site_name, inp))