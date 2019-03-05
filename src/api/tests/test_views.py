from django.test import RequestFactory, TestCase

from mixer.backend.django import mixer
from api.views import MoviesView, CommentsView


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

class CommentListTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.comment1 = mixer.blend('api.Comment')
        self.movie = mixer.blend('api.Movie')
        self.comment2 = mixer.blend('api.Comment', movie_id=self.movie)

    def test_all_comments(self):
        request = self.factory.get('/comments')
        response = CommentsView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 2)

    def test_filtered_comments(self):
        request = self.factory.get('/comments?movie_id=' + str(self.movie.id))
        response = CommentsView.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(len(payload), 1)

class CommentCreateTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.movie1 = mixer.blend('api.Movie')

    def test_add_comment(self):
        request = self.factory.post('/comments', data={'movie_id': self.movie1.id, 'text': 'comment1'})
        response = CommentsView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 201)

    def test_add_comment_when_no_movie(self):
        request = self.factory.post('/comments', data={'movie_id': 111, 'text': 'comment1'})
        response = CommentsView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)
    
    def test_incorrect_id_type(self):
        request = self.factory.post('/comments', data={'movie_id': "wrong", 'text': 'comment1'})
        response = CommentsView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_comment(self):
        request = self.factory.post('/comments', data={'movie_id': self.movie1, 'text': ''})
        response = CommentsView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

        request = self.factory.post('/comments', data={'text': 'asd'})
        response = CommentsView.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, 400)

class TopListView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
       
    def test_missing_params(self):
        request = self.factory.get('/top', data={'start': ""})
        response = TopView.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 400)

        request = self.factory.get('/top', data={'end': ""})
        response = TopView.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_format(self):
        request = self.factory.get('/top', data={'start': "sdfdsf", 'end': "sdfdsfsdf"})
        response = TopView.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 400)

        request = self.factory.get('/top', data={'start': "06-06-2000", 'end': "2000-06-06"})
        response = TopView.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 400)

    def test_valid_request(self):
        request = self.factory.get('/top', data={'start': "06-06-1900", 'end': "01-01-2000"})
        response = TopView.as_view({"get": "list"})(request)
        self.assertEqual(response.status_code, 200)