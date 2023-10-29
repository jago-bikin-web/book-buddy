from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from findbuddy.forms import RatingsForm

@csrf_exempt  # Tambahkan ini jika Anda ingin menonaktifkan proteksi CSRF
def add_rating(request):
    if request.method == 'POST':
        # Dapatkan data yang dikirimkan melalui permintaan POST
        data = request.POST

        # Dapatkan nilai rating dan ID buku
        rating = data.get('rating')
        book_id = data.get('productId')

        if rating is not None and book_id is not None:
            # Dapatkan objek buku
            book = get_object_or_404(Book, pk=book_id)

            # Perbarui nilai average_ratings di model Book
            current_ratings = book.average_rating
            current_ratings_count = book.ratings_count

            new_ratings_count = current_ratings_count + 1
            new_average_ratings = (current_ratings * current_ratings_count + int(rating)) / new_ratings_count

            # Perbarui nilai average_ratings di model Book
            book.average_rating = new_average_ratings
            book.ratings_count = new_ratings_count
            book.save()

            # Kembalikan respons dengan nilai baru average_ratings
            return JsonResponse({'newAverageRating': new_average_ratings})

    # Kembalikan respons dengan kesalahan jika ada kesalahan
    return JsonResponse({'error': 'Failed to add rating'}, status=400)
def show_findbuddy(request):
    books = Book.objects.all()

    form = RatingsForm(request.POST or None)

    categories = set([book.categories for book in books])
    
    context = {
        'name' : 'Gamma',
        'books' : books,
        'categories': categories,
        'form' : form,
    }

    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))

