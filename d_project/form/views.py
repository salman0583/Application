import json
from django.shortcuts import render, redirect
# from .forms import FormModelForm
# from d_project.db import database_connect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import oracledb
import configparser

class tsbdb:
 
    def __init__(self, dbConfig):
        self.dbConfig = dbConfig
        self.connect()
 
    def connect(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.connection = oracledb.connect(
            user=config.get("Database", "username"),
            password=config.get("Database", "password"),
            dsn=config.get("Database", "dsn"),
        )
 
# def database_connect():
#     # Read database configuration from config.ini
#     config = configparser.ConfigParser()
#     config.read("config.ini")
#     dbConfig = {
#         "username": config.get("Database", "username"),
#         "password": config.get("Database", "password"),
#         "dsn": config.get("Database", "dsn"),
#     }
 
#     # Create an instance of tsbdb class
#     tsb_db = tsbdb(dbConfig)
#     print("connected to database!!!!!!")
#     return tsb_db

def database_connect():
    # Read database configuration from config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")
    dbConfig = {
        "username": config.get("Database", "username"),
        "password": config.get("Database", "password"),
        "dsn": config.get("Database", "dsn"),
    }

    # Create an Oracle database connection
    connection = oracledb.connect(
        user=dbConfig["username"],
        password=dbConfig["password"],
        dsn=dbConfig["dsn"]
    )
    return connection

@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            body = json.loads(request.body)
            name = body.get('name')
            email = body.get('email')
            message = body.get('message')

            # Ensure that all required fields are provided
            if not name or not email or not message:
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # Connect to the database
            connection = database_connect()
            cursor = connection.cursor()

            try:
                # Execute the SQL query to insert data into the database
                query = "INSERT INTO FORMS (name, email, message) VALUES (:1, :2, :3)"
                cursor.execute(query, (name, email, message))
                connection.commit()  # Commit the transaction

                # Return success response
                return JsonResponse({"message": "Details saved successfully!"}, status=200)
            except Exception as e:
                print(f"Database Error: {e}")
                return JsonResponse({"error": "An error occurred while saving the data."}, status=500)
            finally:
                cursor.close()
                connection.close()

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
    
@csrf_exempt
def get_forms(request):
    if request.method == 'GET':
        try:
            # Connect to the database
            connection = database_connect()
            cursor = connection.cursor()

            try:
                # Execute the SQL query to fetch data from the database
                query = "SELECT name, email, message FROM FORMS"
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convert query result to a list of dictionaries
                forms_data = [{"name": row[0], "email": row[1], "message": row[2]} for row in rows]

                # Return success response with form data
                return JsonResponse({"forms": forms_data}, status=200)
            except Exception as e:
                print(f"Database Error: {e}")
                return JsonResponse({"error": "An error occurred while fetching the data."}, status=500)
            finally:
                cursor.close()
                connection.close()

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)