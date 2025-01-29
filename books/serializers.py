from rest_framework import serializers
from .models import Book,Publisher
from django.contrib.auth.models import User

class BookSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=200)
    author=serializers.CharField(max_length=200)
  
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Publisher
        fields='__all__'
    
class BookModelSerializer(serializers.ModelSerializer):
    publisher=PublisherSerializer()
    class Meta:
        model=Book
        fields="__all__"
    
    def create(self, validated_data):
        publisher_data = validated_data.pop('publisher')
        publisher,created = Publisher.objects.get_or_create(**publisher_data) 
        book = Book.objects.create(publisher=publisher,**validated_data)
        return book
    
    def update(self, instance, validated_data):
        publisher_data = validated_data.pop('publisher')
        if publisher_data:
            publisher,created=Publisher.objects.get_or_create(**publisher_data)
        instance.title=validated_data.get('title',instance.title)
        instance.author=validated_data.get('author',instance.author)
        instance.published_date=validated_data.get('published_date',instance.published_date)
        instance.save()
        
        return instance
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email']