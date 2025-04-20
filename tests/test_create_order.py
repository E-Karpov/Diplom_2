import allure
import requests

from urls import URL, Endpoints
from data import StatusCode, TextResponse, Ingredients


class TestOrderCreation:
    """
    Тесты для проверки функционала создания заказов.
    Проверяются различные сценарии создания заказа:
    - авторизованный пользователь
    - неавторизованный пользователь
    - с некорректными данными
    """

    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('Проверяем, что авторизованный пользователь может создать заказ с корректными ингредиентами')
    def test_create_order_by_authorized_user_with_valid_ingredients(self, create_new_user):
        """
        Тест проверяет создание заказа авторизованным пользователем с валидными ингредиентами.
        Ожидается успешное создание заказа (статус 200 и success=true в ответе).
        """
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(
            URL.MAIN_URL + Endpoints.CREATE_ORDER,
            headers=headers,
            data=Ingredients.CORRECT_INGREDIENTS_DATA
        )
        assert (response.status_code == StatusCode.OK
                and response.json().get("success") is True)

    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('Проверяем, что неавторизованный пользователь может создать заказ с корректными ингредиентами')
    def test_create_order_by_unauthorized_user_with_valid_ingredients(self):
        """
        Тест проверяет создание заказа неавторизованным пользователем с валидными ингредиентами.
        Ожидается успешное создание заказа (статус 200 и success=true в ответе).
        """
        response = requests.post(
            URL.MAIN_URL + Endpoints.CREATE_ORDER,
            data=Ingredients.CORRECT_INGREDIENTS_DATA
        )
        assert (response.status_code == StatusCode.OK
                and response.json().get("success") is True)

    @allure.title('Проверка создания заказа без ингредиентов')
    @allure.description('Проверяем обработку попытки создания заказа без указания ингредиентов')
    def test_create_order_with_missing_ingredients_fails(self, create_new_user):
        """
        Тест проверяет обработку попытки создания заказа без ингредиентов.
        Ожидается ошибка 400 с соответствующим сообщением.
        """
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(
            URL.MAIN_URL + Endpoints.CREATE_ORDER,
            headers=headers,
            data=Ingredients.INCORRECT_INGREDIENTS_DATA_WITHOUT_FILLING
        )
        assert (response.status_code == StatusCode.BAD_REQUEST
                and response.json().get("success") is False
                and response.json().get("message") == TextResponse.MISSING_FIELDS)

    @allure.title('Проверка создания заказа с невалидным хэшем')
    @allure.description('Проверяем обработку попытки создания заказа с некорректными хэшами ингредиентов')
    def test_create_order_with_invalid_ingredient_hashes_fails(self, create_new_user):
        """
        Тест проверяет обработку попытки создания заказа с невалидными хэшами ингредиентов.
        Ожидается ошибка 500 (Internal Server Error).
        """
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}
        response = requests.post(
            URL.MAIN_URL + Endpoints.CREATE_ORDER,
            headers=headers,
            data=Ingredients.INCORRECT_INGREDIENTS_DATA_HASH
        )
        assert (response.status_code == StatusCode.INTERNAL_SERVER_ERROR
                and TextResponse.SERVER_ERROR in response.text)