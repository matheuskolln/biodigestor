from django.http import HttpResponse, JsonResponse

import json
from biodigestor.models import User

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the biodigestor index.")

def create_user(request):
    # get the data from the request
    if request.method != "POST":
        # show all the users
        users = User.objects.all()
        users_data = []
        for user in users:
            users_data.append({"name": user.name, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at})
        return JsonResponse({"users": users_data})
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    email = body.get("email")
    name = body.get("name")
    password = body.get("password")
    print(email, name, password)

    if not name or not email or not password:
        # return json
        return JsonResponse({"error": "Missing required fields"}, status=400)
    # create the user
    user = User(name=name, email=email, password=password)
    user.save()

    # return the user data without the password and with a message
    return JsonResponse({"message": "User created", "user": {"name": user.name, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at}}, status=201)
