import jwt
import datetime
from django.contrib.auth.models import User

SECRET_KEY = 'X9y$#zL8qR2oH3pE6sW7vB1jM4aU0tD5gF@!K'

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def get_current_user(jwt_token):
    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    current_user = User.objects.get(id=payload['user_id'])
    return current_user

