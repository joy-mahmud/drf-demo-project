from django.urls import path
from . import views 
urlpatterns = [
    path('books/',views.BookListView.as_view(),name="books"),
    path('books-model-list/',views.BookListModelView.as_view(),name="book_model_list"),
]
