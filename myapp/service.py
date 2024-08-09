import square
from square.client import Client
from django.conf import settings

class SquarePaymentService:
    def __init__(self):
        self.client = Client(
            access_token=settings.SQUARE_ACCESS_TOKEN,
            environment='sandbox'  # Change to 'production' for live payments
        )

    def create_payment(self, amount, currency, source_id, idempotency_key, book_title):
        body = {
            "source_id": source_id,
            "idempotency_key": idempotency_key,
            "amount_money": {
                "amount": amount,
                "currency": currency
            },
            "note": f"Payment for {book_title}",
            "autocomplete": True,
        }

        response = self.client.payments.create_payment(body)
        return response