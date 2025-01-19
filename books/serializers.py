from rest_framework import serializers
from .models import Book
class BookSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=200)
    author=serializers.CharField(max_length=200)
    
class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields="__all__"