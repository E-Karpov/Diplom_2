import pytest
import allure
import requests

from helpers import Person
from urls import URL, Endpoints
from data import StatusCode, TextResponse


class TestUserProfileUpdates:
    """Тесты для проверки обновления данных пользователя в системе."""

    @allure.title('Проверка изменения данных с авторизацией')
    @allure.description('Проверка успешного обновления данных профиля для авторизованного пользователя')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_authorized_user_can_update_profile_data(self, create_new_user, data):
        """
        Проверяет возможность авторизованного пользователя изменять:
        - Имя
        - Пароль
        - Email
        Ожидается статус 200 и success=true в ответе.
        """
        # Получаем токен доступа из фикстуры создания пользователя
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}

        # Отправляем запрос на изменение данных
        response = requests.patch(
            URL.MAIN_URL + Endpoints.DATA_CHANGE,
            headers=headers,
            data=data
        )

        # Проверяем успешность операции
        assert (response.status_code == StatusCode.OK
                and response.json().get("success") is True)

    @allure.title('Проверка изменения данных пользователя без авторизации')
    @allure.description('Проверка запрета обновления профиля без авторизации')
    @pytest.mark.parametrize('data', [
        Person.create_data_correct_user()["name"],
        Person.create_data_correct_user()["password"],
        Person.create_data_correct_user()["email"]
    ])
    def test_unauthorized_user_cannot_update_profile(self, data):
        """
        Проверяет, что система запрещает изменение данных профиля:
        - Имени
        - Пароля
        - Email
        без авторизации, возвращая статус 401 и сообщение об ошибке.
        """
        # Отправляем запрос на изменение данных без авторизации
        response = requests.patch(
            URL.MAIN_URL + Endpoints.DATA_CHANGE,
            data=data
        )

        # Проверяем сообщение об ошибке
        assert (response.status_code == StatusCode.UNAUTHORIZED
                and response.json().get("message") == TextResponse.UNAUTHORIZED)