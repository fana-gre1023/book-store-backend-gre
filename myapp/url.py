from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, ReviewViewSet, CreateTransactionView
from . import views

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
book_router = DefaultRouter()
book_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('kids/', include(router.urls)),
    path('kids/books/<int:book_pk>/', include(book_router.urls)),
    path('transactions/', CreateTransactionView.as_view(), name='create-transaction'),
]
