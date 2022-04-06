from werkzeug.security import generate_password_hash, check_password_hash
from services.interfaces.Ipassword_hash import IPassHash
from services.dependency_inject.injector import Services

class PassHash(IPassHash):
    def __init__(self):
        pass
    
    @staticmethod
    def generate_pass(password):
        return generate_password_hash(password)

    @staticmethod
    def check_pass(password, input):
        return check_password_hash(password, input)