from django.db import models
from datetime import datetime


class Book(models.Model):
    book_id = models.CharField(max_length=255)
    etag = models.CharField(max_length=255)
    self_link = models.URLField(max_length=255)

    title = models.CharField(max_length=255)
    authors = models.TextField()
    publisher = models.CharField(max_length=255)
    published_date = models.DateField()
    description = models.TextField()

    isbn_13 = models.CharField(max_length=13)
    isbn_10 = models.CharField(max_length=10)

    page_count = models.IntegerField()
    categories = models.TextField()
    average_rating = models.FloatField()
    ratings_count = models.IntegerField()

    small_thumbnail = models.URLField(max_length=255)
    thumbnail = models.URLField(max_length=255)

    language = models.CharField(max_length=10)
    preview_link = models.URLField(max_length=255)
    infoLink = models.URLField(max_length=255)

    country = models.CharField(max_length=3)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    buyLink = models.URLField(max_length=255)

    webReaderLink = models.URLField(max_length=255)
    accessViewStatus = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @classmethod
    def create_from_json(cls, book_json):
        volume_info = book_json.get("volumeInfo", {})
        sale_info = book_json.get("saleInfo", {})
        access_info = book_json.get("accessInfo", {})

        authors = ", ".join(volume_info.get("authors", []))
        categories = ", ".join(volume_info.get("categories", []))

        published_date=volume_info.get("publishedDate")
        try:
            published_date = datetime.strptime(published_date, '%Y-%m-%d').date()
        except ValueError:
            try:
                published_date = datetime.strptime(published_date, '%Y').date()
            except ValueError:
                published_date = datetime(1, 1, 1).date()


        return cls(
            book_id=book_json.get("id"),
            etag=book_json.get("etag"),
            self_link=book_json.get("selfLink", ""),
            title=volume_info.get("title", ""),
            authors=authors,
            publisher=volume_info.get("publisher", ""),
            published_date=published_date,
            description=volume_info.get("description", ""),
            isbn_13=next(
                (
                    identifier["identifier"]
                    for identifier in volume_info.get("industryIdentifiers", [])
                    if identifier["type"] == "ISBN_13"
                ),
                "",
            ),
            isbn_10=next(
                (
                    identifier["identifier"]
                    for identifier in volume_info.get("industryIdentifiers", [])
                    if identifier["type"] == "ISBN_10"
                ),
                "",
            ),
            page_count=volume_info.get("pageCount", 0),
            categories=categories,
            average_rating=volume_info.get('averageRating', 0),
            ratings_count=volume_info.get('ratingsCount', 0),
            small_thumbnail=volume_info.get(
                "imageLinks", {}).get("smallThumbnail", ""),
            thumbnail=volume_info.get("imageLinks", {}).get("thumbnail", ""),
            language=volume_info.get("language", ""),
            preview_link=volume_info.get("previewLink", ""),
            infoLink=volume_info.get("infoLink", ""),
            country=sale_info.get("country", ""),
            list_price=sale_info.get("listPrice", {}).get("amount", 0.0),
            retail_price=sale_info.get("retailPrice", {}).get("amount", 0.0),
            buyLink=sale_info.get("buyLink", ""),

            webReaderLink=access_info.get("webReaderLink", ""),
            accessViewStatus=access_info.get("accessViewStatus", ""),
        )
