class URL:
    """URL сервиса"""
    MAIN_URL = 'https://stellarburgers.nomoreparties.site'


class Endpoints:
    """Ручки для работы с API"""

    # Аутентификация
    CREATE_USER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    DELETE_USER = '/api/auth/user'
    DATA_CHANGE = '/api/auth/user'

    # Заказы
    CREATE_ORDER = '/api/orders'
    GET_ORDERS = '/api/orders'