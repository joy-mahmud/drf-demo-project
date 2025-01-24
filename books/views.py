from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,filters
from .serializers import BookSerializer,BookModelSerializer,PublisherSerializer

from .models import Book,Publisher

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
    
@api_view(['PUT'])
def update_book(request,id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({'error':'Book not found'},status=404)
    
    serializer = BookModelSerializer(book,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data)
    
    return Response(serializer.errors,status=400)

@api_view(['PATCH'])
def partial_update_book(request,id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({'error':'Book not found'},status=404)
    
    serializer = BookModelSerializer(book,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response (serializer.data)
    
    return Response(serializer.errors,status=400)

@api_view(['DELETE'])
def delete_book(request,id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response({'error':'Book not found'},status=404)
    
    book.delete()
    return Response({'msg':'book deleted successfully'},status=204)

class BookViewsets(viewsets.ModelViewSet):
    queryset=Book.objects.all()
    serializer_class=BookModelSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields=['title','published_date','author']

class PublisherViewset(viewsets.ModelViewSet):
    queryset=Publisher.objects.all()
    serializer_class=PublisherSerializer

    
        