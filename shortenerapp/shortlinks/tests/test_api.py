from django.test import TestCase
from django.test import Client
from shortlinks.models import ShortLink
from shortlinks.utils import validate_url
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

    #TODO: move it from api tests to dedicated test file
    def test_url_validatior(self):
        non_valid_url = "some long non valid string"
        valid_url_1= "http://google.com"
        valid_url_2 = "https://facebook.com"

        non_valid_res = validate_url(non_valid_url)
        valid_res1 = validate_url(valid_url_1)
        valid_res2 = validate_url(valid_url_2)

        self.assertFalse(non_valid_res)
        self.assertTrue(valid_res1)
        self.assertTrue(valid_res2)

    def test_incorrect_url(self):
        sample_url = "some long non valid string"
        data = {
            "url": sample_url
        }
        payload = json.dumps(data)

        response = self.client.post('/create', payload, content_type="application/json")
        #print(response.content, response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), "Mailformed URL")


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


    def test_clicks_increment(self):
        sample_url = "https://google.com"
        data = {
            "url": sample_url
        }
        payload = json.dumps(data)

        response = self.client.post('/create', payload, content_type="application/json")
        short_link = response.content.decode()

        hash = short_link.split("/")[-1]
        self.assertEqual(len(hash), 7)

        obj = ShortLink.objects.get(hash=hash)
        self.assertEqual(obj.origin, sample_url)
        self.assertEqual(obj.clicks, 0)

        response2 = self.client.get('/s/{}'.format(hash), follow=True)
        obj = ShortLink.objects.get(hash=hash) #reloading object from db
        self.assertEqual(obj.clicks, 1)

        response3 = self.client.get('/s/{}'.format(hash), follow=True)
        obj = ShortLink.objects.get(hash=hash) #reloading object from db
        self.assertEqual(obj.clicks, 2)


