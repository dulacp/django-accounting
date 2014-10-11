import decimal


def banker_round(decimal_value):
    """
    Force the value to be rounded with the `ROUND_HALF_EVEN` method,
    also called the Banking Rounding due to the heavy use in the
    banking system
    """
    return decimal_value.quantize(decimal.Decimal('0.01'),
                                  rounding=decimal.ROUND_HALF_EVEN)
