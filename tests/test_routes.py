import unittest
from service import create_app

class AccountRoutesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_health(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_and_read_account(self):
        response = self.client.post("/accounts", json={"name": "Asha", "email": "asha@example.com"})
        self.assertEqual(response.status_code, 201)
        account_id = response.get_json()["id"]
        read_response = self.client.get("/accounts/" + account_id)
        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(read_response.get_json()["name"], "Asha")

    def test_list_accounts(self):
        self.client.post("/accounts", json={"name": "Asha", "email": "asha@example.com"})
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_update_account(self):
        created = self.client.post("/accounts", json={"name": "Asha", "email": "asha@example.com"}).get_json()
        response = self.client.put("/accounts/" + created["id"], json={"name": "Anaya"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Anaya")

    def test_delete_account(self):
        created = self.client.post("/accounts", json={"name": "Asha", "email": "asha@example.com"}).get_json()
        response = self.client.delete("/accounts/" + created["id"])
        self.assertEqual(response.status_code, 204)

if __name__ == "__main__":
    unittest.main()
