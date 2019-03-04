from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer


class MoviesViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.movie1 = mixer.blend('api.Movie')
        self.movie2 = mixer.blend('api.Movie')

    def test_movies(self):
        request = self.factory.get('/movies')
        response = MoviesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 2)
        self.assertTrue(str(self.movies1) in payload)