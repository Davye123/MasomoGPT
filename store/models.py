from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 150, unique=True ,db_index=True)
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class publisher(models.Model):
	name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length=150, unique=True ,db_index=True)
	bio = models.TextField()
	pic = models.FileField(upload_to = "publishher/")
	create_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.name

class Book(models.Model):
    publisher = models.ForeignKey(publisher, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    price = models.IntegerField()
    coverpage = models.FileField(upload_to="coverpage/")
    bookpage = models.FileField(upload_to="bookpage/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    totalreview = models.IntegerField(default=1)
    totalrating = models.IntegerField(default=5)
    description = models.TextField()
    document_type = models.CharField(max_length=10, choices=[('pdf', 'PDF'), ('image', 'Image'), ('text', 'Text'), ('word', 'Word'), ('excel', 'Excel')], default='pdf')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.document_type = self.get_document_type()
        super().save(*args, **kwargs)

    def get_document_type(self):
        ext = self.bookpage.name.split('.')[-1].lower()
        if ext in ['pdf']:
            return 'pdf'
        elif ext in ['jpg', 'jpeg', 'png', 'gif']:
            return 'image'
        elif ext in ['txt']:
            return 'text'
        elif ext in ['doc', 'docx']:
            return 'word'
        elif ext in ['xls', 'xlsx']:
            return 'excel'
        return 'unknown'

class Review(models.Model):
	customer = models.ForeignKey(User, on_delete = models.CASCADE)
	book = models.ForeignKey(Book, on_delete = models.CASCADE)
	review_star = models.IntegerField()
	review_text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
 
 
 

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book') 
