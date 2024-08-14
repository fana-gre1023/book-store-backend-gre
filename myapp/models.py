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
    current = models.TextField(max_length=3)
    signed = models.BooleanField(default=False)
    dated = models.BooleanField(default=False)
    promo = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    statue = models.CharField(max_length=255, default='Available')

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
    
class Address(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.state}"

class Transactions(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    books = models.ManyToManyField('Book', related_name='translations')

    def __str__(self):
        return f'Transaction {self.transaction_id} - {self.amount} {self.currency}'