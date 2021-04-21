def format_integer(integer):
    commma_separated = "{:,}".format(integer)
    period_separated = commma_separated.replace(",", ".")
    return period_separated


def format_pesos(integer):
    formatted_integer = format_integer(integer)
    return f"${formatted_integer}"
