from locust import HttpUser, task, between
import random

class ApiUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://localhost:8008"
    
    def on_start(self):
        """
        Вызывается при старте каждого пользователя.
        """
        self.username = f"user_{random.randint(1000, 9999)}"
        self.password = "password123"
        self.token = None
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": self.username,
                "email": f"{self.username}@test.com",
                "password": self.password
            }
        )
        response = self.client.post(
            "/api/v1/auth/login",
            data={
                "username": self.username,
                "password": self.password
            }
        )
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
        
    @task(3)
    def create_and_read_tasks(self):
        """
        Создает задачу, а затем получает список всех задач.
        """
        if self.token:
            # Создание задачи
            self.client.post(
                "/api/v1/tasks/",
                json={
                    "title": f"Task {random.randint(1, 1000)}",
                    "description": "This is a new test task."
                }
            )

            # Получение списка задач
            self.client.get("/api/v1/tasks/")
            
    @task(1)
    def read_current_user(self):
        """
        Получает информацию о текущем пользователе.
        """
        if self.token:
            self.client.get("/api/v1/users/me")