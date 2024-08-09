from django.contrib.auth.decorators import user_passes_test


def superuser_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = 'some_default_url' 

    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator