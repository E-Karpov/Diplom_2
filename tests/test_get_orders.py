import allure
import requests

from urls import URL, Endpoints
from data import StatusCode, TextResponse, Ingredients


class TestOrderRetrieval:
    """Тесты для проверки получения информации о заказах пользователя."""

    @allure.title('Проверка получения заказов авторизованным пользователем')
    @allure.description('Проверка, что авторизованный пользователь может получить список своих заказов')
    def test_authorized_user_can_get_orders(self, create_new_user):
        """Проверяет, что система возвращает список заказов для авторизованного пользователя
        и что номер созданного заказа присутствует в списке."""
        # Получаем токен из фикстуры создания пользователя
        token = create_new_user[1].json()["accessToken"]
        headers = {'Authorization': token}

        # Создаем тестовый заказ
        response_create_order = requests.post(
            URL.MAIN_URL + Endpoints.CREATE_ORDER,
            headers=headers,
            data=Ingredients.CORRECT_INGREDIENTS_DATA
        )

        # Получаем список заказов
        response_get_order = requests.get(
            URL.MAIN_URL + Endpoints.GET_ORDERS,
            headers=headers
        )

        # Проверяем статус код и соответствие номера заказа
        assert (response_get_order.status_code == StatusCode.OK
                and response_create_order.json()["order"]["number"]
                == response_get_order.json()["orders"][0]["number"])

    @allure.title('Проверка получения заказов неавторизованным пользователем')
    @allure.description('Проверка, что неавторизованный пользователь не может получить список заказов')
    def test_unauthorized_user_cannot_get_orders(self):
        """Проверяет, что система возвращает ошибку 401 и корректное сообщение
        при попытке получения списка заказов без авторизации."""
        response_get_order = requests.get(URL.MAIN_URL + Endpoints.GET_ORDERS)
        assert (response_get_order.status_code == StatusCode.UNAUTHORIZED
                and response_get_order.json().get("message") == TextResponse.UNAUTHORIZED)