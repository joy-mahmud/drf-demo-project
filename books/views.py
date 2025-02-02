from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,filters
from .serializers import BookSerializer,BookModelSerializer,PublisherSerializer,UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from .models import Book,Publisher
from django.contrib.auth.models import User

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

    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['title','published_date','author']
    search_fields=['title','author']

class PublisherViewset(viewsets.ModelViewSet):
    queryset=Publisher.objects.all()
    serializer_class=PublisherSerializer
 
@api_view(['POST'])    
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        hashPassword=make_password(request.data['password'])
        newUser = serializer.save(password=hashPassword)
        
        token = Token.objects.create(user=newUser)
        return Response({'token':token.key,'user':serializer.data})
    return Response(serializer.errors,status=400)

@api_view(['POST']) 
def login(request):
    user=User.objects.get(username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'details':'invalid credentials'},status=404)
    
    token,created = Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({'token':token.key,'user':serializer.data})

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'message':"user successfully logged out"}, status=200)
    except Exception:
        return Response({'error':"something went wrong"},status=500)
    
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def testToken(request):
    return Response({'msg':"passed"})
    
    

    
        