from django.shortcuts import render
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

