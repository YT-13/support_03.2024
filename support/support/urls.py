import time

import httpx
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

cached_rate = None
last_request_time = None


@csrf_exempt
def get_exchange_rate(request):

    global cached_rate, last_request_time

    if last_request_time is not None and time.time() - last_request_time < 10:
        return JsonResponse({"rate": cached_rate})

    source_currency = request.POST.get("source_currency", "")
    destination_currency = request.POST.get("destination_currency", "")
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={source_currency}&to_currency={destination_currency}&apikey=V2V43QAQ8RILGBOW"

    try:
        response = httpx.get(url)
        response.raise_for_status()
    except httpx.HTTPError:
        return JsonResponse(
            {"error": "Failed to fetch exchange rate."}, status=500
        )

    try:
        data = response.json()
        cached_rate = data["Realtime Currency Exchange Rate"][
            "5. Exchange Rate"
        ]
        last_request_time = time.time()
        return JsonResponse({"rate": cached_rate})
    except (KeyError, ValueError):
        return JsonResponse({"error": "Failed to parse response."}, status=500)


urlpatterns = [
    path("exchange-rate/", get_exchange_rate, name="exchange_rate"),
]
