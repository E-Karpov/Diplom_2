import pytest
import allure
import requests

from helpers import Person
from urls import URL, Endpoints
from data import StatusCode, TextResponse


class TestUserRegistration:
    """Тесты для проверки регистрации пользователей в системе."""

    @allure.title('Проверка создания уникального пользователя')
    @allure.description('Проверка успешной регистрации нового пользователя с валидными данными')
    def test_successful_user_registration(self, create_new_user):
        """Проверяет, что система корректно регистрирует нового пользователя
        и возвращает статус 200 и флаг success=true."""
        response = create_new_user
        assert response[1].json().get("success") == True and response[1].status_code == StatusCode.OK

    @allure.title('Проверка создания дублирующего пользователя')
    @allure.description('Проверка невозможности регистрации пользователя с уже существующими учетными данными')
    def test_duplicate_user_registration(self, create_new_user):
        """Проверяет, что система возвращает ошибку 403 и корректное сообщение
        при попытке зарегистрировать уже существующего пользователя."""
        response = create_new_user
        payload = response[0]
        response_double_register = requests.post(URL.MAIN_URL + Endpoints.CREATE_USER, data=payload)
        assert response_double_register.status_code == StatusCode.FORBIDDEN and (
            response_double_register.json().get("message") == TextResponse.CREATE_DOUBLE_USER
            )

    @allure.title('Проверка создания пользователя с некорректными данными')
    @allure.description('Проверка валидации обязательных полей при регистрации пользователя')
    @pytest.mark.parametrize('payload', [
        Person.create_data_incorrect_user_without_email(),
        Person.create_data_incorrect_user_without_name(),
        Person.create_data_incorrect_user_without_password()
    ])
    def test_registration_with_missing_required_fields(self, payload):
        """Проверяет, что система возвращает ошибку 403 и флаг success=false
        при попытке регистрации без обязательных полей (email, имя, пароль)."""
        response = requests.post(URL.MAIN_URL + Endpoints.CREATE_USER, data=payload)
        assert response.status_code == StatusCode.FORBIDDEN and response.json().get("success") == False