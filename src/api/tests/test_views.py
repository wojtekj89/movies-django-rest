from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer
from api.views import MoviesView


class MoviesListTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.movie1 = mixer.blend('api.Movie')
        self.movie2 = mixer.blend('api.Movie')

    def test_movies(self):
        request = self.factory.get('/movies')
        response = MoviesView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 2)
        self.assertTrue(str(self.movie1) in str(payload))

class MoviesCreateTest(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        self.movie2 = mixer.blend('api.Movie', title="Existing")
        self.title = 'mock'
    
    def test_add_movie(self):
        request = self.factory.post('/movies', data={'title': self.title})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)
        payload = response.data
        self.assertTrue(self.title in str(payload).lower())
    
    def test_add_existing_movie(self):
        request = self.factory.post('/movies', data={'title': "Existing"})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 409)
        payload = response.data
        self.assertEqual(len(payload), 1)

    def test_add_without_title(self):
        request = self.factory.post('/movies', data={'asd': self.title})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_create_existing_short_title(self):
        movie = mixer.blend('api.Movie', title="Game of Thrones")
        request = self.factory.post('/movies', data={'title': "Game"})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 409)

    
class MovieCreateAndGetTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.title = "Test"

    def test_add_and_read(self):
        request = self.factory.get('/movies')
        response = MoviesView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 0)

        request = self.factory.post('/movies', data={'title': self.title})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)

        request = self.factory.get('/movies')
        response = MoviesView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 1)
        self.assertTrue(self.title in str(payload))

