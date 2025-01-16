from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
# Create your views here.
class BookListView(APIView):
    def get(self,request):
        books=[
            {'title':"The great gatsby",'author':'F. scott'},
            {'title':'To kill a mokingbird', 'author':'Harper Lee'}
        ]
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)