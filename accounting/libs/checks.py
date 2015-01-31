from django.core.validators import EMPTY_VALUES
from django.utils.datastructures import SortedDict


class PrimaryKeyRelatedField(object):
    pass


class CheckResult(object):
    """
    Stands for a checking result of a model field
    """

    RESULT_NEUTRAL = 'neutral'
    RESULT_FAILED = 'failed'
    RESULT_PASSED = 'passed'
    RESULT_CHOICES = (
        (RESULT_NEUTRAL, "Neutral"),
        (RESULT_FAILED, "Failed"),
        (RESULT_PASSED, "Passed"),
    )

    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'
    LEVEL_CHOICES = (
        (LEVEL_WARNING, "Warning"),
        (LEVEL_ERROR, "Error"),
    )

    def __init__(self, field, result=None, level=None, message=None):
        self.field = field
        self.message = message

        if not result:
            result = self.RESULT_NEUTRAL
        self.result = result

        if not level:
            level = self.LEVEL_WARNING
        self.level = level

    def mark_fail(self, level=LEVEL_WARNING, message=None):
        self.result = self.RESULT_FAILED
        self.level = level
        self.message = message

    def mark_pass(self, message=None):
        self.result = self.RESULT_PASSED
        self.message = message

    @property
    def has_failed(self):
        return self.result == self.RESULT_FAILED

    @property
    def has_passed(self):
        return self.result == self.RESULT_PASSED


class CheckingModelOptions(object):
    """
    Meta class options for `CheckingModelMixin`
    """
    def __init__(self, meta):
        self.fields = getattr(meta, 'fields', ())
        assert isinstance(self.fields, (list, tuple)), \
            '`fields` must be a list or tuple'

        self.exclude = getattr(meta, 'exclude', ())
        assert isinstance(self.exclude, (list, tuple)), \
            '`exclude` must be a list or tuple'


class CheckingModelMixin(object):

    _options_class = CheckingModelOptions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts = self._options_class(getattr(self, 'CheckingOptions', None))

    def has_custom_check_for_field(self, field_name):
        return hasattr(self, 'check_%s' % field_name)

    def get_check_for_field(self, field_name, checking_fields=None):
        if checking_fields is None:
            checking_fields = self.get_checking_fields()

        if field_name not in checking_fields:
            raise AttributeError("Field '%s' not checkable" % field_name)

        field = checking_fields.get(field_name)
        check = CheckResult(field=field)

        # custom check method
        if self.has_custom_check_for_field(field_name):
            return getattr(self, 'check_%s' % field_name)(check)

        # default check
        if isinstance(field, PrimaryKeyRelatedField):
            value = getattr(self, field_name).all()
            has_failed = bool(value.count() == 0)
        else:
            value = getattr(self, field_name)
            has_failed = bool(value in EMPTY_VALUES)

        if has_failed:
            check.mark_fail()
        else:
            check.mark_pass()
        return check

    def get_checking_fields(self, special_exclude=['id']):
        """
        Returns the set of fields on which we perform checkings
        """
        ret = SortedDict()
        for f in self._meta.fields:
            # avoid special_exclude fields
            if f.attname in special_exclude:
                continue
            ret[f.attname] = f

        # Deal with reverse relationships
        reverse_rels = self._meta.get_all_related_objects()
        # reverse_rels += self._meta.get_all_related_many_to_many_objects()
        for relation in reverse_rels:
            accessor_name = relation.get_accessor_name()
            to_many = relation.field.rel.multiple
            if not self.opts.fields or accessor_name not in self.opts.fields:
                continue
            if not to_many:
                raise NotImplementedError
            ret[accessor_name] = PrimaryKeyRelatedField()

        # If 'fields' is specified, use those fields, in that order.
        if self.opts.fields:
            new = SortedDict()
            for key in self.opts.fields:
                new[key] = ret[key]
            ret = new

        # Remove anything in 'exclude'
        if self.opts.exclude:
            for key in self.opts.exclude:
                ret.pop(key, None)

        return ret

    def check_fields(self):
        """
        First `self.clean_fields` is called to ensure data integrity

        Checks all fields and return a list of `CheckResult` instances
        """
        # TODO try to reintegrate this one without
        #      increase the db queries too much
        # self.clean_fields()

        checks = []
        fields = self.get_checking_fields()
        for key, field in fields.items():
            check = self.get_check_for_field(key, checking_fields=fields)
            checks.append(check)
        return checks

    def full_check(self):
        """
        Calls `self.check_fields`, `self.check` in that order

        NB: no need to call `self.full_clean` because the above
            methods already made those calls internally
        """
        # basic field checks
        checks = self.check_fields()

        # special checks
        additional_checks = self.check_additionnals()
        checks.extend(additional_checks)

        return checks

    def check_additionnals(self):
        """Additional checks that the user can implement"""
        return []

    def _raw_checking_completion(self):
        """
        Useful for additional checking completion computations
        """
        checks = self.full_check()
        completed = sum(1 for c in checks if c.has_passed)
        return completed, len(checks)

    def checking_completion(self):
        """
        Compute the percentage of checking completed
        on the model instance
        """
        completed, total = self._raw_checking_completion()
        return float(completed) / total

    def full_checking_completion(self):
        """
        Calls `self.checking_completion`

        This method should be used to do checking completion on
        related objects
        """
        completion = self.checking_completion()
        return completion

    def pass_full_checking(self):
        completion = self.full_checking_completion()
        return completion == 1.0
