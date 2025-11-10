from django.urls import path
from .views import *


urlpatterns = [
    path('book-create/', book_create, name='book_create'),
    path('book-update/<int:book_id>/', book_update, name='book_update'),
    path('book-details/', book_details, name='book_details'),
    path('book-list/', book_list, name='book_list'),
    path('book-search/', book_search, name='book_search'),
    path('book-delete/<int:book_id>/', book_delete, name='book_delete'),
    path('category-list/', category_list, name='category_list'),
    path('books-by-category/<int:category_id>/', books_by_category, name='books_by_category'),
    path('add-comment/<int:book_id>/', add_comment, name='add_comment'),
    path('edit_comment/<int:book_id>/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('votes_book/<int:book_id>/', votes_book, name='book_crvotes_bookeate'),
    path('popular-books/', popular_books, name='popular_books'),
    path('user-books/', user_books, name='user_books'),
]
