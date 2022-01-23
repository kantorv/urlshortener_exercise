from django.test import TestCase
from shortlinks.models import ShortLink



class TestModelCreation(TestCase):
    def test_model_created(self):
        link = ShortLink()
        link.origin = "https://google.com"
        link.save()

        self.assertIsNotNone(link.hash)
        self.assertTrue(len(link.hash)==7)



        link2 = ShortLink()
        link2.origin = "https://facebook.com/somegroup"
        link2.save()

        self.assertTrue(len(link2.hash) == 7)
        self.assertNotEqual(link.hash, link2.hash)


    def test_counter_increment(self):
        link = ShortLink()
        link.origin = "https://google.com"
        link.save()

        self.assertEqual(link.clicks, 0)

        link.increment_clicks()
        self.assertEqual(link.clicks, 1)


