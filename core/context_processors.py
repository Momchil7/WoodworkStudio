def add_profile_to_context(request):
    """
    Adds the currently logged-in user's profile to the template context.
    """
    if request.user.is_authenticated:
        return {'profile': request.user}
    return {'profile': None}
