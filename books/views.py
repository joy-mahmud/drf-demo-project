from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer,BookModelSerializer
from .models import Book
# Create your views here.
class BookListView(APIView):
    def get(self,request):
        books=[
            {'title':"The great gatsby",'author':'F. scott'},
            {'title':'To kill a mokingbird', 'author':'Harper Lee'}
        ]
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)

class BookListModelView(APIView):
    def get(self,request):
        books = Book.objects.all()
        serializer=BookModelSerializer(books,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=BookModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
        