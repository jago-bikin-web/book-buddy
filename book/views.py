import json
import requests

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import Book

def add_book_from_google_books_api(request):
    api_key = "AIzaSyAw208PayHnE8-2khMn5JLGL9bCJTMXJFg"

    """
        fiction = bumi, pulang (20) 
        computers = indonesia, java+python (20)
        --- 39

        science (20)
        --- 59

        cooking (10)
        adventure (10)
        action (10)
        history (10)
        --- 98

        random
        --- 100
    """

    query = {
        "fiction" : ["bumi", "pulang"],
        "computers" : ["indonesia", "java+python"],
    }

    for subject in query:
        for q in query[subject]:
            api_url = f"https://www.googleapis.com/books/v1/volumes?q={q}+subject:{subject}&orderBy=newest&key={api_key}"

            response = requests.get(api_url)

            if response.status_code == 200:
                book_data = json.loads(response.text)
                
                books = book_data.get('items')
                for book in books:
                    book = Book.create_from_json(book)
                    book.save()
            else:
                return JsonResponse({'message': 'Gagal mengambil data dari API Google Books.'}, status=400)


    api_url = f"https://www.googleapis.com/books/v1/volumes?q=subject:science&orderBy=newest&maxResults=20&key={api_key}"

    response = requests.get(api_url)
    if response.status_code == 200:
        book_data = json.loads(response.text)
        
        books = book_data.get('items')
        for book in books:
            book = Book.create_from_json(book)
            book.save()
    else:
        return JsonResponse({'message': 'Gagal mengambil data dari API Google Books.'}, status=400)


    subjects = ["cooking", "adventure", "action", "history"]

    for subject in subjects:
        api_url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{subject}&orderBy=newest&key={api_key}"
        response = requests.get(api_url)

        if response.status_code == 200:
            book_data = json.loads(response.text)
            
            books = book_data.get('items')
            for book in books:
                book = Book.create_from_json(book)
                book.save()

        else:
            return JsonResponse({'message': 'Gagal mengambil data dari API Google Books.'}, status=400)

    api_url = f"https://www.googleapis.com/books/v1/volumes?q=random&orderBy=newest&key={api_key}&maxResults=40"
    response = requests.get(api_url)

    if response.status_code == 200:
        book_data = json.loads(response.text)
        
        books = book_data.get('items')
        for i in range(100 - len(data_books)):
            book = books[i]
            book = Book.create_from_json(book)
            book.save()

    else:
        return JsonResponse({'message': 'Gagal mengambil data dari API Google Books.'}, status=400)
    
    data_books = Book.objects.all()
    print(len(data_books))
    return JsonResponse({'message': 'Data buku berhasil dimasukkan ke dalam database.'})

    
def get_books(request):
    books = Book.objects.all()
    return HttpResponse(serializers.serialize("json", books), content_type="application/json")