def mask_email(email):
    def _mask(value):
        size = len(value)
        if size <= 1:
            return value
        elif size > 1 and size <= 4:
            stars = size - 1
            return "%s%s" % (value[0], "*" * stars)
        elif size > 4 and size <= 6:
            stars = size - 2
            return "%s%s%s" % (value[0], "*" * stars, value[-1])
        else:
            stars = size - 3
            return "%s%s%s" % (value[:2], "*" * stars, value[-1])

    name, domain = email.split("@")
    domain_parts = domain.split(".")
    return "@".join([_mask(name), ".".join([_mask(part) for part in domain_parts])])
