from django.db import models

class Books(models.Model):
    book_id	=models.IntegerField(null=False,blank=False)
    books_count =models.IntegerField(null=False,blank=False)
    isbn=models.CharField(max_length=100, blank=True)
    isbn13=models.CharField(max_length=100,null=False,blank=False)
    authors=models.CharField(max_length=150, blank=True)
    original_publication_year=models.IntegerField(null=False,blank=False)
    original_title=models.CharField(max_length=100, blank=True)
    title=models.CharField(max_length=200, blank=True)
    language_code=models.CharField(max_length=10, blank=True)
    average_rating=models.FloatField(max_length=5,default=2.5)
    ratings_count=models.IntegerField(null=False,blank=False)
    image_url=models.CharField(max_length=100, blank=True)
    small_image_url=models.CharField(max_length=100, blank=True)
    location=models.CharField(max_length=10, blank=True)
    class Meta:
        ordering = ['-average_rating']