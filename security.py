from models.user import UserModel
from werkzeug.security import safe_str_cmp


# User authentication function
def authentication(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# Identity function for user payload
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
