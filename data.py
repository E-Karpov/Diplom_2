class StatusCode:
    """HTTP статус-коды для тестов"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class TextResponse:
    """Текстовые ответы сервера"""
    CREATE_DOUBLE_USER = 'User already exists'
    SERVER_ERROR = 'Internal Server Error'
    UNAUTHORIZED = 'You should be authorised'
    INVALID_CREDENTIALS = 'email or password are incorrect'
    MISSING_FIELDS = 'Ingredient ids must be provided'


class Ingredients:
    """Данные для создания заказов"""
    CORRECT_INGREDIENTS_DATA = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
    }

    INCORRECT_INGREDIENTS_DATA_HASH = {
        "ingredients": ["60d3b41abdacsdf6a733c6", "609646e4dcsfdf0276b2870"]
    }

    INCORRECT_INGREDIENTS_DATA_WITHOUT_FILLING = {
        "ingredients": []
    }


class UserTestData:
    """Тестовые данные пользователей"""
    @staticmethod
    def get_valid_user():
        return {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }

    @staticmethod
    def get_invalid_user_missing_email():
        return {
            "password": "password123",
            "name": "Test User"
        }