from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import stripe
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer, TransactionSerializer, AddressSerializer
from .service import SquarePaymentService
from django.db.models import Avg

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def get_all_books(self, request):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'])
    def get_book_by_id(self, request, pk=None):
        try:
            book = get_object_or_404(Book, pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_pk')
        if book_id:
            return Review.objects.filter(book_id=book_id)
        return Review.objects.all()

    @action(detail=True, methods=['post'])
    def create_review(self, request, book_pk=None):
        try:
            data = request.data
            data['book'] = book_pk
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()

                book = Book.objects.get(pk=book_pk)
                avg_score = Review.objects.filter(book=book).aggregate(Avg('rating'))['rate_avg']
                book.rate = avg_score
                book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['delete'])
    def delete_review(self, request, pk=None):
        try:
            review = get_object_or_404(Review, pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTransactionView(views.APIView):
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        source_id = request.data.get('source_id')
        book_ids = request.data.get('book_ids',[])
        address_datas = request.data.get('address', {})
        idempotency_key = request.data.get('idempotency_key')
        
        address_serializer = AddressSerializer(data=address_datas)
        if address_serializer.is_valid():
            address_serializer.save()
        else:
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        books = Book.objects.filter(id__in=book_ids)
        if len(books) != len(book_ids):
            return Response({"error": "One or more books not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        square_service = SquarePaymentService()
        book_titles = ", ".join(book.title for book in books)
        response = square_service.create_payment(amount, currency, source_id, idempotency_key, book_titles)

        if response.is_success():
            transaction_data = {
                "transaction_id": response.body['payment']['id'],
                "amount": amount,
                "currency": currency,
                "status": response.body['payment']['status'],
                "address":address_datas.id
            }
            serializer = TransactionSerializer(data=transaction_data)
            if serializer.is_valid():
                serializer.save()
                for book in books:
                    book.stock -= 1
                    book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": response.errors}, status=status.HTTP_400_BAD_REQUEST)