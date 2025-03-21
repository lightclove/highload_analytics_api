from locust import HttpUser, task, between

class AnalyticsUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def track_event(self):
        payload = {
            "user_id": 42,
            "event_type": "page_view",
            "timestamp": 1690000000,
            "payload": {"url": "/test"}
        }
        self.client.post("/event", json=payload)
