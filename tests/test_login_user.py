import allure
import requests

from helpers import Person
from urls import URL, Endpoints
from data import StatusCode, TextResponse


class TestUserAuthentication:
    """Тесты для проверки аутентификации пользователей в системе."""

    @allure.title('Проверка входа существующего пользователя')
    @allure.description(
        'Проверка успешной аутентификации зарегистрированного пользователя с валидными учетными данными')
    def test_successful_login_with_valid_credentials(self, create_new_user):
        """
        Проверяет, что система корректно авторизует существующего пользователя,
        возвращает статус 200 и флаг success=true.
        """
        # Получаем данные созданного пользователя из фикстуры
        user_data = create_new_user[0]

        # Выполняем запрос на авторизацию
        login_response = requests.post(URL.MAIN_URL + Endpoints.LOGIN, data=user_data)

        # Проверяем статус код и успешность операции
        assert (login_response.status_code == StatusCode.OK
                and login_response.json().get("success") is True)

    @allure.title('Проверка входа с неверными учетными данными')
    @allure.description('Проверка обработки системы при попытке входа с некорректными учетными данными')
    def test_failed_login_with_invalid_credentials(self):
        """
        Проверяет, что система возвращает ошибку 401, флаг success=false
        и корректное сообщение при попытке входа с неверными учетными данными.
        """
        # Генерируем данные несуществующего пользователя
        invalid_user_data = Person.create_data_incorrect_user_without_name()

        # Выполняем запрос на авторизацию
        login_response = requests.post(
            URL.MAIN_URL + Endpoints.LOGIN,
            data=invalid_user_data
        )

        # Проверяем статус код, флаг успешности и сообщение об ошибке
        assert (login_response.status_code == StatusCode.UNAUTHORIZED
                and login_response.json().get("success") is False
                and login_response.json().get("message") == TextResponse.INVALID_CREDENTIALS)