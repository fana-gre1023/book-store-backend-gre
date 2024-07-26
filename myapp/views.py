from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
import json
from .models import Book, Review, Transactions
from .forms import TransactionForm
from .serializers import BookSerializer, ReviewSerializer

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

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        form = TransactionForm(data)
        if form.is_valid():
            try:
                charge = stripe.Charge.create(
                    amount=int(form.cleaned_data['amount'] * 100),
                    currency=form.cleaned_data['currency'],
                    source=form.cleaned_data['stripe_token'],
                    description=f"Charge for {form.cleaned_data['book'].title}"
                )

                transaction = form.save()
                
                return JsonResponse({
                    'id': transaction.id,
                    'amount': transaction.amount,
                    'currency': transaction.currency,
                    'book': transaction.book.title,
                    'created_at': transaction.created_at
                }, status=201)
            except stripe.error.StripeError as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def list_transactions(request):
    transactions = Transactions.objects.all().values('id', 'amount', 'currency', 'book__title', 'created_at')
    return JsonResponse(list(transactions), safe=False)
