from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, Serializer, CharField
from .models import Movie


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'genre', 'country', 'plot')

class MovieRequestSerializer(Serializer):
    """Checking if POST request is valid """
    title = CharField(max_length=100, required=True)

    def create(self, data):
        return {'title': data.get('title')}

    def update(self, instance, data):
        instance['title'] = data.get('title', instance['title'])