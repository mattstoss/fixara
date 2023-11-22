from django.contrib.auth import authenticate, login, logout


def do_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is None:
        return None
    login(request, user)
    return user


def do_logout(request):
    logout(request)