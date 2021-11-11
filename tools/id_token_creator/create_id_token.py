import sys

from firebase_admin.credentials import Certificate
from firebase_admin.auth import create_custom_token
from firebase_admin import App, initialize_app

credentials = Certificate('../../api/produce-exchange-hub-firebase-adminsdk-ufzci-78e6592558.json')
options = {"databaseURL": "https://produce-exchange-hub.firebaseio.com"}

app = initialize_app(credentials, options, __name__)

if len(sys.argv) < 2:
    raise Exception('Missing argument')

uid = sys.argv[1]

token = create_custom_token(uid, app=app)
print(str(token))
