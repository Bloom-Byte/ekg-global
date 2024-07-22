from ipaddress import ip_address


def get_ip_address(request):
    """Get the requestor's IP address form the Django request object"""
    if not hasattr(request, "META"):
        raise ValueError("Request object must have a 'META' attribute")

    ip = request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_FORWARDED_FOR")
    return ip_address(ip)
