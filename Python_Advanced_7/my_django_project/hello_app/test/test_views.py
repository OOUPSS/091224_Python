from django.test import TestCase
from django.urls import reverse

class HelloViewTest(TestCase):
    def test_hello_view(self):
        # Проверяем, что страница 'hello' отдает правильный ответ
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, your_name")
