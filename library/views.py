from django.shortcuts import render, redirect

from .forms import BookForm
from .models import Book

# Create your views here.

def lib(request):
    books = Book.objects.all()
    return render(request,
                  'library/library.html',
                  context={
                      'books': books
                  }
    )

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request,
                   'library/book_detail.html',
                    context={'book':book}
                  )



def book_create(request):
    bookform = BookForm(request.POST, request.FILES)
    if bookform.is_valid():
        book = bookform.save(commit=False)
        book.save()
        return redirect('/library')
    else:
        bookform = BookForm()
    return  render(request,
                   'library/bookform.html',
                   context={'bookform': bookform}
                   )