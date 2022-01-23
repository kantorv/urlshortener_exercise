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


    def test_same_origin(self):
        link1 = ShortLink(origin = "https://google.com")
        link1.save()

        link2 = ShortLink(origin = "https://google.com")
        link2.save()

        self.assertNotEqual(link1.hash, link2.hash)
