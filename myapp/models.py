from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    coverurl = models.TextField()
    rate = models.FloatField()

    def __str__(self):
        return self.title
class Review(models.Model):
    id = models.TextField(primary_key=True)
    user = models.CharField(max_length=200)
    rating = models.FloatField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} - Rating: {self.rating}"
    
class Transactions(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3)
    stripe_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction for {self.book.title} on {self.created_at}'