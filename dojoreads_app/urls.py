from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('books', views.books),
    path('login', views.login),
    path('logout', views.logout),
    path('books/add', views.add_book),
    path('books/<int:book_id>', views.one_book),
    path('add_review', views.add_review),
    path('users/<int:user_id>', views.user),
    path('delete/<int:review_id>/<int:book_id>', views.delete_review)
]