from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            email = json_data["email"]
            response_data = {}
            result = True
            if email and User.objects.filter(email=email).exists():
                result = False
            response_data['unique'] = result
            return JsonResponse(response_data)
        except KeyError:
            response_data = {}
            response_data['result'] = 'error'
            response_data['message'] = 'wrong data'
            return JsonResponse(response_data, status=500)

