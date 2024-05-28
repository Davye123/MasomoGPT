from django.contrib import admin
from .models import Category, publisher, Book

# Register your models here.



class AddCategory(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, AddCategory)

class Addpublisher(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(publisher, Addpublisher)

class AddBook(admin.ModelAdmin):
	list_display = ['name', 'price', 'created', 'updated']
	list_filter = ['created', 'updated']
	list_editable = ['price']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Book, AddBook)

