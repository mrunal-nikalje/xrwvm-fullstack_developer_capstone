from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CarMake, CarModel
from django.http import JsonResponse
from .populate import initiate

# -------------------------------
# LOGIN VIEW
# -------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("userName")   # MUST be userName
            password = data.get("password")

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return JsonResponse({
                    "userName": username,
                    "status": "Authenticated"   # ⚠️ IMPORTANT (lab expects this)
                })

            else:
                return JsonResponse({
                    "userName": "",
                    "status": "Not Authenticated"
                })

        except Exception as e:
            return JsonResponse({
                "status": "Error",
                "message": str(e)
            }, status=500)

    return JsonResponse({"status": "Invalid request"}, status=400)


# -------------------------------
# LOGOUT VIEW
# -------------------------------
@csrf_exempt
def logout_user(request):
    if request.method == "POST" or request.method == "GET":
        logout(request)
        return JsonResponse({
            "userName": "",
            "status": "Logged out"
        })

    return JsonResponse({"status": "Invalid request"}, status=400)


def get_cars(request):

    count = CarMake.objects.filter().count()
    
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})    