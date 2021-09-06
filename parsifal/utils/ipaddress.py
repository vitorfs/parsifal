def get_remote_ip_address(request):
    meta = getattr(request, "META", {})
    forwarded_for = meta.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[0]
    else:
        ip_address = meta.get("X_REAL_IP", meta.get("REMOTE_ADDR"))
    return ip_address
