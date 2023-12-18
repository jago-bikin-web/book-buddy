import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from book.models import Book
from findbuddy.models import BookFind
from findbuddy.forms import BookForm
from main.models import Profile
from django.db.models import Q

# Create your views here.
def show_json(request):
    data = BookFind.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


@login_required(login_url='main:login')
def show_findbuddy(request):
    books = Book.objects.all()
    form = BookForm(request.POST or None)
    categories = set([book.categories for book in books])
    user = Profile.objects.get(user=request.user)
    profile_picture = user.profile_picture

    context = {
        'books' : books,
        'categories': categories,
        'form': form,
        'user': user.full_name,
        'profile_picture': profile_picture,
    }

    return render(request, "findbuddy.html", context)

def get_book_json(request):
    book_item = Book.objects.all()
    return HttpResponse(serializers.serialize('json', book_item))

@csrf_exempt
def add_request_ajax(request):
    user = Profile.objects.get(user=request.user)
    if user.is_member():
        if request.method == 'POST':
            title = request.POST.get("title")
            author = request.POST.get("author")

            new_request = BookFind(title=title, author=author)
            new_request.save()

            return HttpResponse(b"CREATED", status=201)
        return HttpResponseNotFound()


def get_request_json(request):
    request_item = BookFind.objects.all()
    return HttpResponse(serializers.serialize('json', request_item))


def get_search_books(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        filter = request.GET.get('filter', '')

        print(filter)

        if (filter == " All "):
            filter = ""

        results = Book.objects.filter(title__contains=query, categories__contains=filter)

        return HttpResponse(serializers.serialize('json', results))

@csrf_exempt
def create_request_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Periksa apakah pengguna yang membuat permintaan sesuai dengan pemilik produk
        if request.user.is_authenticated:
            new_product = BookFind.objects.create(
                title=data["title"],
                author=data["author"]
            )
            return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)