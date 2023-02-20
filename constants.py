URL = "http://127.0.0.1:3000/api/upload"
CSV_FILE_NAME = 'vehicles.csv'
HEADERS = {'Content-Type': 'application/json'}

LOGIN_PAYLOAD = {
    "username": "365",
    "password": "1"
}
LOGIN_HEADERS = {
    "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json"
}
COLOR_ENDPOINT = 'https://api.baubuddy.de/dev/index.php/v1/labels/'
LOGIN_ENDPOINT = "https://api.baubuddy.de/index.php/login"
VEHICLES_ENDPOINT = (
    'https://api.baubuddy.de/dev/index.php/v1/vehicles/'
    'select/active/'
)
