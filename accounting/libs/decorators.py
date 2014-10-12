# encoding: utf-8


def composed(*decs):
    """
    Compose multiple decorators

    Example :

    >>> @composed(dec1, dec2)
    ...     def some(f):
    ...         pass
    """
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def order_fields(*field_list):
    def decorator(form):
        original_init = form.__init__

        def init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            for field in field_list[::-1]:
                self.fields.insert(0, field, self.fields.pop(field))
        form.__init__ = init
        return form
    return decorator
