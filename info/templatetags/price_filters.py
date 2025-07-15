from django import template

register = template.Library()

@register.filter
def format_inr(value):
    try:
        value = int(value)

        if value >= 10_000_000:
            crores = value // 10_000_000
            lakhs = (value % 10_000_000) // 100_000

            if lakhs > 0:
                return f"{crores} Cr {lakhs} Lakh"
            else:
                return f"{crores} Cr"

        elif value >= 100_000:
            lakhs = value // 100_000
            remainder = value % 100_000
            decimal = remainder / 100_000
            result = round(lakhs + decimal, 1)
            return f"{result} Lakh"

        else:
            return f"{value:,}" 

    except (TypeError, ValueError):
        return value
