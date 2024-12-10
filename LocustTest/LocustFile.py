from locust import HttpUser, task, between

class ApiTestUser(HttpUser):
    wait_time = between(1, 3)  # Simulate waiting between 1 and 3 seconds

    @task
    def predict(self):
        # Prepare a file to send to the API with the specific file path
        image_path = r"C:\\COOLYEAH\\SEM7\\TKTB\\TKTBMLOPS\\LocustTest\\07SteroidPerioral.jpg"
        with open(image_path, "rb") as image_file:
            files = {"file": ("07SteroidPerioral.jpg", image_file, "image/jpeg")}
            response = self.client.post("/predict", files=files)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")

    @task
    def index(self):
        self.client.get("/")
