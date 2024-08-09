from django.shortcuts import render, HttpResponse
from user_accounts.models import CustomUser
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

# fetch all users
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, "admin_dashboad/dashboard.html", context)


# delete user url
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, id):
    if request.method == 'DELETE':
        user = CustomUser.objects.get(id=id)
        user.delete()
        return HttpResponse(status=204)  # No Content
    return HttpResponse(status=405)  # Method Not Allowed