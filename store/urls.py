from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
 path('', views.index, name = "index"),
 path('login', views.signin, name="signin"),
 path('logout', views.signout, name="signout"),
 path('registration', views.registration, name="registration"),
 path('books', views.get_books, name='books'),
 path('category/<int:id>/',views.get_book_category, name='get_book_category'),
 path('book/<int:id>', views.get_book, name="book"),
 path('search/', views.search, name = "search"),
 path('publisher/<int:id>', views.get_publisher, name = "publisher"),
 path('add_to_favorites/<int:book_id>/',views.add_to_favorites, name='add_to_favorites'),
 path('remove_from_favorites/<int:book_id>/',views.remove_from_favorites, name='remove_from_favorites'),
 path('favorites/',views.favorite_books, name='favorite_books'),
]