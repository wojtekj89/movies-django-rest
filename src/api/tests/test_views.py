from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer
from api.views import MoviesView


class MoviesViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.movie1 = mixer.blend('api.Movie')
        self.movie2 = mixer.blend('api.Movie')
        print(str(self.movie1))

    def test_movies(self):
        request = self.factory.get('/movies')
        response = MoviesView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 2)
        self.assertTrue(str(self.movie1) in str(payload))