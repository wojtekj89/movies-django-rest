from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.response import Response

from django.db import IntegrityError

from django.shortcuts import get_object_or_404

from .models import Movie, Comment
from .serializers import MovieSerializer, MovieRequestSerializer, CommentSerializer

from .services import get_movie

class MoviesView(ListModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        request = MovieRequestSerializer(data=request.data)

        if not request.is_valid():
            return Response(request.errors, status=HTTP_400_BAD_REQUEST)

        title = request.data['title']

        try:
            omdb_data = get_movie(title)
        except:
            return Response({'error': 'OMDB API error'}, status=HTTP_503_SERVICE_UNAVAILABLE)
            
        movie = Movie(
            title=omdb_data['Title'], 
            year=omdb_data['Year'], 
            genre=omdb_data['Genre'],
            country=omdb_data['Country'],
            plot=omdb_data['Plot']
            )

        if Movie.objects.filter(title=omdb_data['Title']).exists():
            return Response({'error': 'Movie already exists'}, status=HTTP_409_CONFLICT)

        try:
            movie.save()
        except:
            return Response({'error': ''}, status=HTTP_409_CONFLICT)

        return Response(MovieSerializer(movie).data, status=HTTP_201_CREATED)

class CommentsView(ListModelMixin, GenericViewSet, CreateModelMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Optionally filter to `movie_id` passed in querystring."""
        queryset = Comment.objects.all()
        movie_id = self.request.query_params.get('movie_id', None)
        if movie_id is not None:
            try:
                movie_id = int(movie_id)
            except ValueError:
                raise exceptions.ValidationError({
                    'movie_id': [
                        'Incorrect movie_id type. Expected int.',
                    ],
                })
            movie = get_object_or_404(Movie, id=movie_id)
            queryset = queryset.filter(movie_id=movie)
        return queryset