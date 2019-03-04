from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer, CharField
from .models import Movie


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'genre', 'country', 'plot')