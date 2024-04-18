from django.core.mail import EmailMessage

from .helpers import get_currency_vn
from .template_mail import *

def mail_content_order(order_code, 
                       name, 
                       email,
                       phone, 
                       address, 
                       total_order, 
                       items_order_mail, 
                       link_order_check):
    order_items = ''
    for item in items_order_mail:
        item["price"] = get_currency_vn(item["price"])
        item["total"] = get_currency_vn(item["total"])
        order_items += TEMPLATE_ORDER_ITEMS.substitute(item)

    html_content = TEMPLATE_ORDER.substitute(
        order_code=order_code, 
        name=name, 
        email=email, 
        phone=phone, 
        address=address, 
        total_order=get_currency_vn(total_order), 
        order_items=order_items,
        link_order_check=link_order_check
    )

    return html_content

def mail_content_contact(name, email, phone, message):
    html_content = TEMPLATE_CONTACT.substitute(
        name=name,
        email=email,
        phone=phone,
        message=message,
    )
    return html_content

def send_mail(subject, content, email_to, email_bcc=[]):
    email_message = EmailMessage(
        subject, 
        content,
        to=email_to, 
        bcc=email_bcc,
        # cc = receivers will see cc, but not bcc
        # http_message=""
    )
    email_message.content_subtype = "html"
    email_message.send()
