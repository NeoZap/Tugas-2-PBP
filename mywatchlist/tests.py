from django.test import TestCase

class MyWatchListTests(TestCase):
    def test_html_endpoint(self):
        resp = self.client.get("/mywatchlist/html/")
        self.assertEqual(resp.status_code, 200)

    def test_json_endpoint(self):
        resp = self.client.get("/mywatchlist/json/")
        self.assertEqual(resp.status_code, 200)

    def test_xml_endpoint(self):
        resp = self.client.get("/mywatchlist/xml/")
        self.assertEqual(resp.status_code, 200)