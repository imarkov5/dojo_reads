from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def books(request):
    if 'name' in request.session:
        context={
            'last_3_reviews': Review.objects.all().order_by('-id')[:3],
            'all_books': Book.objects.all()
        }
        return render(request, 'books_home.html', context)
    return redirect('/')

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashed_password = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hashed_password)
    request.session['user_id'] = new_user.id
    request.session['name'] = new_user.name
    request.session['alias'] = new_user.alias
    return redirect('/books')

def login(request):
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
            request.session['name'] = logged_user.name
            request.session['alias'] = logged_user.alias
            request.session['user_id'] = logged_user.id
            return redirect('/books')
        else: 
            messages.error(request, "Wrong password!")
            return redirect('/')
    else:
        messages.error(request, "Wrong email!")
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_book(request):
    context = {
        'all_authors': Author.objects.all()
    }
    if request.method == 'POST':
        existing_author = Author.objects.filter(author=request.POST['author'])
        if len(existing_author) > 0:
            this_author = existing_author[0]
        else:
            this_author = Author.objects.create(author=request.POST['new_author'])
        book = Book.objects.create(title=request.POST['title'], author=this_author)
        Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, poster=User.objects.get(id=request.session['user_id']))
        book_id = book.id
        return redirect(f'/books/{book_id}')
    return render(request, 'add_book.html', context)
    # if request.method == 'POST':
    #     existing_author = Author.objects.filter(author=request.POST['author'])
    #     if len(existing_author) > 0:
    #         existing_author = existing_author[0]
    #         print(existing_author.author)
    #         book = Book.objects.create(title=request.POST['title'], author=existing_author)
    #         Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, poster=User.objects.get(id=request.session['user_id']))
    #         book_id = book.id
    #         return redirect(f'/books/{book_id}')
    #     else:
    #         this_author = Author.objects.create(author=request.POST['new_author'])
    #         book = Book.objects.create(title=request.POST['title'], author=this_author)
    #         Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=book, poster=User.objects.get(id=request.session['user_id']))
    #         book_id = book.id
    #         return redirect(f'/books/{book_id}')
    # return render(request, 'add_book.html', context)

def one_book(request, book_id):
    book = Book.objects.get(id=book_id)
    context ={
        'book': Book.objects.get(id=book_id),
        'all_reviews': book.reviews.all()
    }
    return render(request, 'one_book.html', context)

def add_review(request):
    this_book = Book.objects.get(id=request.POST['book_id'])
    this_user = User.objects.get(id=request.session['user_id'])
    book_id = request.POST['book_id']
    if len(request.POST['review']) < 5:
        messages.error(request, "Review must be at least 5 characters!")
        return redirect(f'/books/{book_id}')
    Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=this_book, poster=this_user)
    return redirect(f'/books/{book_id}')

def user(request, user_id):
    current_user = User.objects.get(id=user_id)
    # user_reviews = current_user.reviews.all()
    # print(user_reviews[0].book.title)
    context={
        'user': current_user,
        'user_reviews': current_user.reviews.all()
    }
    return render(request, 'user.html', context)

def delete_review(request, review_id, book_id):
    review_to_delete = Review.objects.get(id=review_id)
    review_to_delete.delete()
    return redirect(f'/books/{book_id}')