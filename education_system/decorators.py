from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        @user_passes_test(lambda u: u.is_authenticated and u.role == role, login_url='/login/')
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('login')
        return _wrapped_view
    return decorator
