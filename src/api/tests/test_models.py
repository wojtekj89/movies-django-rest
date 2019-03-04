from django.test import TestCase
import pytest

from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestModels(TestCase):

    def test_movie_model(self):
        movie = mixer.blend('api.Movie')
        self.assertEqual(movie.pk, 1)

    def test_comment_model(self):
        comment = mixer.blend('api.Comment')
        self.assertEqual(comment.pk, 1)

    def test_movie_string_representation(self):
        movie = mixer.blend('api.Movie')
        self.assertEqual(movie.title, str(movie))