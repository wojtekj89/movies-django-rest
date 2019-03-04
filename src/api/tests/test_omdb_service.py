from django.test import TestCase

from unittest.mock import Mock, patch

from requests.exceptions import RequestException

from api.services import get_movie

class OMDBTest(TestCase):

    def test_real_request(self):
        r = get_movie('django')

        self.assertEqual(r['Title'], 'Django')

    @patch('api.services.requests.get')
    def test_exception(self, mock_service):
        """ Test if OMDB error is thrown """
        mock_service.side_effect = RequestException()
        with self.assertRaises(RequestException):
            get_movie('django')
