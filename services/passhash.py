from werkzeug.security import generate_password_hash, check_password_hash

class PassHash:

    @staticmethod
    def generate_pass(password):
        return generate_password_hash(password)

    @staticmethod
    def check_pass(password, input):
        return check_password_hash(password, input)