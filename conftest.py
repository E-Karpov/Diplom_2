import pytest
import requests
from helpers import Person
from urls import URL, Endpoints
from data import StatusCode, TextResponse


@pytest.fixture
def create_new_user():
    """Фикстура для создания и удаления тестового пользователя"""
    payload = Person.create_data_correct_user()

    response = requests.post(
        f"{URL.MAIN_URL}{Endpoints.CREATE_USER}",
        json=payload
    )

    if response.status_code != StatusCode.OK:
        pytest.fail(f'Ошибка при создании пользователя: {response.text}')

    yield payload, response

    token = response.json().get('accessToken')
    if token:
        delete_response = requests.delete(
            f"{URL.MAIN_URL}{Endpoints.DELETE_USER}",
            headers={'Authorization': token}
        )
        assert delete_response.status_code == StatusCode.ACCEPTED


def pytest_make_parametrize_id(val):
    """Функция для корректного отображения параметров в отчетах"""
    return repr(val)