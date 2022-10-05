import unittest
import json
import requests


API_URL = 'http://localhost:8000/process/'


def call_api(endpoint, text):
    url = API_URL + endpoint
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"type": "text", "content": text})
    return requests.post(url, headers=headers, data=payload).json()


class TestEndpoint(unittest.TestCase):

    def setUp(self):
        self.endpoint = "wrong"
        self.text = "Filipas gyvena Vilniuje. "

    def test_invalid_endpoint(self):
        response = call_api(self.endpoint, self.text)
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.service.not.found')


class TestTaggerIntegration(unittest.TestCase):

    def setUp(self):
        self.endpoint = "tagger"
        self.text = "Filipas gyvena Vilniuje. "

    def test_tagger_response_type(self):
        response = call_api(self.endpoint, self.text)
        self.assertEqual(response["response"]["type"], 'annotations')

    def test_tagger_response_content(self):
        response = call_api(self.endpoint, self.text)
        for entity in ("PROPN", "VERB", "PUNCT"):
            self.assertIn(entity, [t["features"]["pos"] for t in response["response"]["annotations"]["token"]])
        self.assertIn("sentence", response["response"]["annotations"])

    def test_tagger_with_empty_request(self):
        response = call_api(self.endpoint, "")
        self.assertIn('annotations', response["response"])

    def test_tagger_with_too_large_request(self):
        large_text = self.text * 601
        response = call_api(self.endpoint, large_text)
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.request.too.large')

    def test_tagger_with_long_token(self):
        long_token = "A" * 10000
        response = call_api(self.endpoint, long_token)
        self.assertIn('annotations', response["response"])

    def test_tagger_with_special_characters(self):
        spec_text = "\N{grinning face}\u4e01\u0009" + self.text + "\u0008"
        response = call_api(self.endpoint, spec_text)
        gpe = [t for t in response["response"]["annotations"]["token"] if t["features"]["pos"] == "PROPN"][1]
        self.assertEqual(spec_text[gpe["start"]:gpe["end"]], "Vilniuje")


class TestNERIntegration(unittest.TestCase):

    def setUp(self):
        self.endpoint = "ner"
        self.text = "Filipas gyvena Vilniuje. "

    def test_ner_response_type(self):
        response = call_api(self.endpoint, self.text)
        self.assertEqual(response["response"]["type"], 'annotations')

    def test_ner_response_content(self):
        response = call_api(self.endpoint, self.text)
        for entity in ("PERSON", "LOC"):
            self.assertIn(entity, response["response"]["annotations"])

    def test_ner_with_empty_request(self):
        response = call_api(self.endpoint, "")
        self.assertIn('annotations', response["response"])

    def test_ner_with_too_large_request(self):
        large_text = self.text * 601
        response = call_api(self.endpoint, large_text)
        self.assertEqual(response['failure']['errors'][0]['code'],
                         'elg.request.too.large')

    def test_ner_with_long_token(self):
        long_token = "A" * 10000
        response = call_api(self.endpoint, long_token)
        self.assertIn('annotations', response["response"])

    def test_ner_with_special_characters(self):
        spec_text = "\N{grinning face}\u4e01\u0009" + self.text + "\u0008"
        response = call_api(self.endpoint, spec_text)
        gpe = response["response"]["annotations"]["LOC"][0]
        self.assertEqual(spec_text[gpe["start"]:gpe["end"]], "Vilniuje")


if __name__ == '__main__':
    unittest.main()
