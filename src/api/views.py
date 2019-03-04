from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer, MovieRequestSerializer

from .services import get_movie

class MoviesView(ListModelMixin, GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        request = MovieRequestSerializer(data=request.data)

        if not request.is_valid():
            return Response(request.errors, status=HTTP_400_BAD_REQUEST)

        title = request.data['title']

        if Movie.objects.filter(title=title).exists():
            return Response({'error': 'Movie already exists'}, status=HTTP_409_CONFLICT)

        omdb_data = get_movie(title)
        movie = Movie(
            title=omdb_data['Title'], 
            year=omdb_data['Year'], 
            genre=omdb_data['Genre'],
            country=omdb_data['Country'],
            plot=omdb_data['Plot']
            )

        movie.save()

        return Response(MovieSerializer(movie).data, status=HTTP_201_CREATED)