from django.test import TestCase

from api.services import get_movie

class OMDBTest(TestCase):

    def test_real_request(self):
        r = get_movie('django')

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Title'], 'Django')