from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views 

router=DefaultRouter()
router.register(r'book-viewset',views.BookViewsets)
router.register(r'publishers',views.PublisherViewset)
urlpatterns = [
    path('books/',views.BookListView.as_view(),name="books"),
    path('books-model-list/',views.BookListModelView.as_view(),name="book_model_list"),
    path('update-book/<int:id>/',views.update_book,name="update_book"),
    path('partial-update-book/<int:id>/',views.partial_update_book,name="partial_update_book"),
    path('delete-book/<int:id>/',views.delete_book,name='delete_book'),
    
    path('',include(router.urls))
]
