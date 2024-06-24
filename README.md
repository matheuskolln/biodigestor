# Biodigestor Server
This is the server for the biodigestor project. It is a REST API that allows the client to interact with the biodigestor and perform actions such as reading the data and posting into the database.

# Prerequisites

- Python 3.x
- Django 3.x or higher
- A database (PostgreSQL is recommended)

# Installation

1. Clone the repository
```bash
git clone https://github.com/matheuskolln/biodigestor
cd biodigestor
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Apply the migrations
```bash
python manage.py migrate
```

5. Run the server
```bash
python manage.py runserver
```

# Models

The server has three models: `User`, `Biodigestor` and `Measurement`.

## User

The `User` model is used to authenticate the client. It has the following fields:

- `name`: The user's name
- `email`: The user's email
- `password`: The user's password
- `created_at`: The date and time the user was created
- `updated_at`: The date and time the user was last updated

## Biodigestor

The `Biodigestor` model represents the biodigestor. It has the following fields:

- `name`: The biodigestor's name
- `description`: A description of the biodigestor
- `created_at`: The date and time the biodigestor was created
- `updated_at`: The date and time the biodigestor was last updated

## Measurement

The `Measurement` model represents a measurement taken from the biodigestor. It has the following fields:

- `internal_temperature`: The internal temperature of the biodigestor
- `external_temperature`: The external temperature of the biodigestor
- `main_pressure`: The main pressure of the biodigestor
- `gas_level`: The gas level of the biodigestor
- `created_at`: The date and time the measurement was taken
- `updated_at`: The date and time the measurement was last updated

# Views

The server has three views: `UserView`, `BiodigestorView` and `MeasurementView`.

## UserView

The `UserView` is used to create, read, update and delete users. It has the following endpoints:

- `GET /users/`: Get a list of all users
- `POST /users/`: Create a new user: `name`, `email` and `password` are required

## BiodigestorView

The `BiodigestorView` is used to create, read, update and delete biodigestors. It has the following endpoints:

- `GET /biodigestors/`: Get a list of all biodigestors
- `POST /biodigestors/`: Create a new biodigestor: `name` and `description` are required

## MeasurementView

The `MeasurementView` is used to create, read, update and delete measurements. It has the following endpoints:

- `GET /measurements/`: Get a list of all measurements
- `POST /measurements/`: Create a new measurement: `internal_temperature`, `external_temperature`, `main_pressure` and `gas_level` are required
