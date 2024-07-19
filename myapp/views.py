from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from.models import Book
from.serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class BookViewSet(viewsets.ModelViewSet): 
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def get_all_books(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_by_id(self, request, pk=None):
        book = self.get_object()
        serializer = BookSerializer(book)
        return Response(serializer.data)