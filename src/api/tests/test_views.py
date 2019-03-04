from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer
from api.views import MoviesView


class MoviesListTest(TestCase):

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
        self.assertEqual(len(payload), 2)
        self.assertTrue(self.title in str(payload).lower())
    
    def test_add_existing_movie(self):
        request = self.factory.post('/movies', data={'title': self.title})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(len(payload), 1)


    def test_add_without_title(self):
        request = self.factory.post('/movies', data={'asd': self.title})
        response = MoviesView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(payload), 1)
