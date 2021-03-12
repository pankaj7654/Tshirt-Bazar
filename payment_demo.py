from instamojo_wrapper import Instamojo
API_KEY = "test_1a27dbe7c32079fe70e91d6fd9a"
AUTH_TOKEN = 'test_436036c4a50adb8b5bd2462dd65'

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, 
endpoint='https://test.instamojo.com/api/1.1/');
response = api.payment_request_create(
    amount='11',
    purpose='Testing',
    send_email=True,
    email="pkumarpandit25@gmail.com",
    redirect_url="http://localhost:8000/handle_redirect"
    )

print(response['payment_request']['longurl'])