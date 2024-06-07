from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
import json
from biodigestor.models import BioDigestor, Measurement, User

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the biodigestor index.")

def users(request):
    # get the data from the request
    if request.method == "GET":
        # show all the users
        users = User.objects.all()
        users_data = []
        for user in users:
            users_data.append({"name": user.name, "email": user.email, "created_at": user.created_at, "updated_at": user.updated_at})
        return JsonResponse({"users": users_data})
    if request.method == "POST":
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
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
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

def biodigestor(request):
    return HttpResponse("Hello, world. You're at the biodigestor index.")

def biodigestors(request):
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        name = body.get("name")
        description = body.get("description")

        biodigestor = BioDigestor(name=name, description=description)
        biodigestor.save()

        return JsonResponse({"message": "BioDigestor created", "biodigestor": {"name": biodigestor.name, "description": biodigestor.description, "created_at": biodigestor.created_at, "updated_at": biodigestor.updated_at}}, status=201)
    if request.method == "GET":
        biodigestors = BioDigestor.objects.all()
        biodigestors_data = []
        for biodigestor in biodigestors:
            biodigestors_data.append({"name": biodigestor.name, "description": biodigestor.description, "created_at": biodigestor.created_at, "updated_at": biodigestor.updated_at})
        return JsonResponse({"biodigestors": biodigestors_data})
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)

def measurements(request):
    if request.method == "GET":
        measurements = Measurement.objects.all()
        measurements_data = []
        for measurement in measurements:
            measurements_data.append({"internal_temperature": measurement.internal_temperature, "external_temperature": measurement.external_temperature, "main_pressure": measurement.main_pressure, "gas_level": measurement.gas_level, "created_at": measurement.created_at, "updated_at": measurement.updated_at})
        return JsonResponse({"measurements": measurements_data})
    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        internal_temperature = body.get("internal_temperature")
        external_temperature = body.get("external_temperature")
        main_pressure = body.get("main_pressure")
        gas_level = body.get("gas_level")

        measurement = Measurement(internal_temperature=internal_temperature, external_temperature=external_temperature, main_pressure=main_pressure, gas_level=gas_level)
        measurement.save()

        return JsonResponse({"message": "Measurement created", "measurement": {"internal_temperature": measurement.internal_temperature, "external_temperature": measurement.external_temperature, "main_pressure": measurement.main_pressure, "gas_level": measurement.gas_level, "created_at": measurement.created_at, "updated_at": measurement.updated_at}}, status=201)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
