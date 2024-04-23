import frappe
from frappe import _
from frappe.utils.data import today, date_diff, get_datetime_str
import json

def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """
    expiry = frappe.db.get_single_value('Limiting Doc', 'site_expiry_date')
    email = frappe.db.get_single_value('Limiting Doc', 'support_email')
    phone = frappe.db.get_single_value('Limiting Doc', 'support_phone')
    print(expiry)

    diff = date_diff(expiry, today())
    if login_manager.user != "Administrator" and diff < 0:
        frappe.throw(_("Your account has been suspended as your subscription has expired. <br> Contact our billing & sales team as per below details and make payment to renew your subscription <br> Email: {0} <br>Phone: {1}").format(email,phone), frappe.AuthenticationError)

def user_limit(self, method):
    allow_users = frappe.db.get_single_value('Limiting Doc', 'no_of_users')
    print(allow_users)

# get active users

    user_list = frappe.get_list('User', filters={'enabled': 1,"name":['not in',['Guest', 'Administrator']]})
    active_users = len(user_list)
    print(active_users)

# get email and phone from limit doctype

    email = frappe.db.get_single_value('Limiting Doc', 'support_email')
    phone = frappe.db.get_single_value('Limiting Doc', 'support_phone')

    if allow_users != 0 and active_users > allow_users:
        frappe.throw(_("Purchased User Licened {0},Creating{1} User <br> You can not create additional user or contact our sales & billing team as per below details and make payment for additional users. <br>Email{2} <br> Phone:{3}  ").format(allow_users,active_users,email,phone))


    # Company

    def company_limit(self, method):
        '''validate company limit'''

        # get no of company from Limiting Doc
        allowed_companies= frappe.db.get_list('Limiting Doc',"no_of_companies")
        print(allowed_companies)

        # calculatin total companies

        total_company = int(frappe.db.get_value('Company',filters={}))
        print(total_company)

        # get email and phone from limiting doc

        email = frappe.db.get_value('Limiting Doc','support_email')
        contact = frappe.db.get_value('Limiting Doc','support_phone')

        # validations

        if allowed_companies != 0 and total_company >= allowed_companies:
            frappe.throw(_("Purchased Subsidiary Licenses: {}<br>You have {} company(s).<br>You cannot create additionl company/subsidiary as you have reached the limit of active subsidiaries subscription you have purchased.<br>Please disable some of the active subsidiaries if not required or contact our sales & billing team as per below details and make payment for subsidiary.<br>Email: {}<br> Phone: {}").format(allowed_companies, total_company,email,phone))  