from django.http import JsonResponse
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("userName")
            password = data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # ✅ IMPORTANT: match frontend expectation
                return JsonResponse({
                    "userName": username,
                    "status": "success"
                })

            else:
                return JsonResponse({
                    "userName": "",
                    "status": "fail",
                    "message": "Invalid username or password"
                }, status=200)

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)


def logout_user(request):
    logout(request)  # terminate session
    data = {"userName": ""}
    return JsonResponse(data)