from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import json

from .models import CarMake, CarModel
from .populate import initiate

# Import API helpers (Lab 4)
from .restapis import get_request, analyze_review_sentiments, post_review


# -------------------------------
# LOGIN VIEW
# -------------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            username = data.get("userName")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    "userName": username,
                    "status": "Authenticated"
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
    if request.method in ["POST", "GET"]:
        logout(request)
        return JsonResponse({
            "userName": "",
            "status": "Logged out"
        })

    return JsonResponse({"status": "Invalid request"}, status=400)


# -------------------------------
# GET CARS
# -------------------------------
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


# -------------------------------
# GET DEALERS
# -------------------------------
def get_dealerships(request, state="All"):

    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealers": dealerships
    })


# -------------------------------
# GET DEALER DETAILS
# -------------------------------
def get_dealer_details(request, dealer_id):

    endpoint = "/fetchDealer/" + str(dealer_id)
    dealer = get_request(endpoint)

    return JsonResponse({
        "status": 200,
        "dealer": dealer
    })


# -------------------------------
# GET DEALER REVIEWS + SENTIMENT
# -------------------------------
def get_dealer_reviews(request, dealer_id):

    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    # Add sentiment safely
    if reviews:
        for review in reviews:
            review["sentiment"] = "neutral"   # default value

            try:
                sentiment_response = analyze_review_sentiments(
                    review.get("review", ""))

                if sentiment_response and "sentiment" in sentiment_response:
                    review["sentiment"] = sentiment_response["sentiment"]

            except Exception as e:
                print("Sentiment error:", e)
                review["sentiment"] = "neutral"

    return JsonResponse({
        "status": 200,
        "reviews": reviews
    })

# -------------------------------
# ADD REVIEW (POST)
# -------------------------------


@csrf_exempt
def add_review(request):

    if not request.user.is_anonymous:

        if request.method == "POST":
            try:
                data = json.loads(request.body)

                post_review(data)

                return JsonResponse({
                    "status": 200,
                    "message": "Review posted successfully"
                })

            except Exception as e:
                return JsonResponse({
                    "status": 401,
                    "message": "Error posting review",
                    "error": str(e)
                })

    return JsonResponse({
        "status": 403,
        "message": "Unauthorized"
    })
