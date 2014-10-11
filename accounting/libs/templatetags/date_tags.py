# encoding: utf-8

from django import template

from apps.catalogue.models import OpeningPeriod
from classytags.core import Tag, Options
from classytags.arguments import Argument


register = template.Library()


class EarlyDateCalculator(Tag):
    name = 'get_early_date'
    options = Options(
        Argument('opening_period'),
        Argument('additional_minutes', required=False, default=0),
        )

    def render_tag(self, context, opening_period, additional_minutes):
        early_date = opening_period.early_date(additional_minutes)
        if early_date:
            return early_date.strftime('%H:%M')
        return None

register.tag(EarlyDateCalculator)


class LateDateCalculator(Tag):
    name = 'get_late_date'
    options = Options(
        Argument('opening_period'),
        Argument('additional_minutes', required=False, default=0),
        )

    def render_tag(self, context, opening_period, additional_minutes):
        late_date = opening_period.late_date(additional_minutes)
        if late_date:
            return late_date.strftime('%H:%M')
        return None

register.tag(LateDateCalculator)