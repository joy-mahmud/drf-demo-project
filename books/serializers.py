from rest_framework import serializers
from .models import Book,Publisher
class BookSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=200)
    author=serializers.CharField(max_length=200)
    
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        fields='__all__'
    
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"