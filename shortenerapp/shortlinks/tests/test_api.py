from django.test import TestCase
from django.test import Client
from shortlinks.models import ShortLink
import json


class TestApi(TestCase):
    def setUp(self):
        self.client = Client()


    def test_link_creation(self):
        sample_url = "https://google.com"
        data = {
            "url": sample_url
        }
        payload = json.dumps(data)

        response = self.client.post('/create', payload, content_type="application/json")
        #print(response.content, response.status_code)
        self.assertEqual(response.status_code, 201)

    def test_incorrect_url(self):
        sample_url = "some long string"
        data = {
            "url": sample_url
        }
        payload = json.dumps(data)

        response = self.client.post('/create', payload, content_type="application/json")
        #print(response.content, response.status_code)
        self.assertEqual(response.status_code, 201)


    def test_redirect_chain(self):
        sample_url = "https://google.com"
        data = {
            "url": sample_url
        }
        payload = json.dumps(data)

        response = self.client.post('/create', payload, content_type="application/json")
        short_link = response.content.decode()

        redirected_response = self.client.get(short_link, follow=True)
        redirect_chain = redirected_response.redirect_chain[0]
        redirect_url, status_code = redirect_chain

        self.assertEqual(status_code, 302)
        self.assertEqual(redirect_url, sample_url)


    def test_non_existing_url(self):
        non_existing_suffix = "abcdefg"
        response = self.client.get('/s/{}'.format(non_existing_suffix), follow=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(),'link not found')



