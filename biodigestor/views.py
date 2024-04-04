from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
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

    # check if exists a user with the same email
    user = User.objects.filter(email=email).first()
    if user:
        return JsonResponse({"error": "User already exists"}, status=400)
    print(email, name, password)

    if not name or not email or not password:
        # return json
        return JsonResponse({"error": "Missing required fields"}, status=400)

    user = User(name=name, email=email, password=make_password(salt='batatinha', password=password))
    user.save()

    # return the user data without the password and with a message
    return JsonResponse({"message": "User created", "user": {"name": user.name, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at}}, status=201)

def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    email = body.get("email")
    password = make_password(salt='batatinha', password=body.get("password"))

    user = User.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    return JsonResponse({"message": "User logged in", "user": {"name": user.name, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at}})
