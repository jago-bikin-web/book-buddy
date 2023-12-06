from random import randint

from django.http import JsonResponse

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from main.models import Profile


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                user_login = Profile.objects.get(user=user)
                response = JsonResponse({
                    "username": user_login.full_name,
                    "status": True,
                    "message": "Login sukses!"
                }, status=200)
                response.set_cookie('user', user_login.full_name)
                return response
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Akun telah dinonaktifkan."
                }, status=401)

        else:
            return JsonResponse({
                "status": False,
                "message": "Periksa kembali email atau kata sandi."
            }, status=400)
    else:
        return JsonResponse({
            "status": False,
            "message": "Method tidak ditemukan!"
        }, status=405)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        status = request.POST.get("status")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        print(request.POST)
        print(full_name)
        print(username)
        print(email)
        print(status)
        print(password1)
        print(password2)

        if password1 == password2:
            try:
                user = User.objects.filter(username=username)
                if len(user) == 0:
                    user = User.objects.create_user(
                        username=username, password=password1)

                    new_user = Profile(user=user, full_name=full_name, email=email, status=status,
                                       profile_picture=f"https://i.pravatar.cc/48?img={randint(1, 70)}")

                    new_user.save()
                    login(request, user)
                    return JsonResponse({
                        "username": new_user.full_name,
                        "status": True,
                        "message": "Register sukses!"
                    }, status=200)

                else:
                    return JsonResponse({
                        "status": False,
                        "message": "Username sudah pernah dibuat!"
                    }, status=400)
            except:
                return JsonResponse({
                    "status": False,
                    "message": "Server error."
                }, status=500)

        else:
            return JsonResponse({
                "status": False,
                "message": "Password tidak sama!"
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Method tidak ditemukan!"
        }, status=405)


@csrf_exempt
def logout(request):

    try:
        username = request.user.username
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout gagal!"
        }, status=401)
