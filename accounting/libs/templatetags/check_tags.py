from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import InclusionTag

register = template.Library()


@register.tag
class Check(InclusionTag):
    name = 'render_check'
    template = '_generics/check_tag.html'
    options = Options(
        Argument('check'),
    )

    def get_context(self, context, check):
        context.update({
            'check': check
        })

        return context
