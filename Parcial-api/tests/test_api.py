import unittest
from api.app import create_app

class VaccinationApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_get_data_by_year(self):
        response = self.app.get("/api/vaccination/year/2018")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))

if __name__ == "__main__":
    unittest.main()
