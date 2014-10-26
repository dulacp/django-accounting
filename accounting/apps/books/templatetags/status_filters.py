from django import template

register = template.Library()


@register.filter('status_to_css_classname')
def _invoice_or_bill_status_to_classname(invoice_or_bill):
    """
    Return the appropriated css classname for the invoice/bill status
    """
    if not invoice_or_bill.pass_full_checking():
        checks = invoice_or_bill.full_check()
        for c in checks:
            if c.level == c.LEVEL_ERROR:
                return 'danger'
        return 'warning'

    if invoice_or_bill.is_fully_paid():
        return 'success'
    elif invoice_or_bill.is_partially_paid():
        return 'info'
    else:
        return ''
