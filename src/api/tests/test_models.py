from django.test import TestCase

from mixer.backend.django import mixer

class TestModels(TestCase):

    def test_movie_model(self):
        movie = mixer.blend('api.Movie')
        self.assertGreaterEqual(movie.pk, 1)

    def test_comment_model(self):
        comment = mixer.blend('api.Comment')
        self.assertGreaterEqual(comment.pk, 1)

    def test_movie_string_representation(self):
        movie = mixer.blend('api.Movie')
        self.assertEqual(movie.title, str(movie))