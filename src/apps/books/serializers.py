from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    ...


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catregory
        fields = "name",


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    books_category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = "title", "author","books_category", "published_date", "book_image", "language", "slug"

    def create(self, validated_data):
        title = validated_data.get('title')
        author = validated_data.get('author')
        published_date = validated_data.get('published_date')
        book_image = validated_data.get('book_image')
        language = validated_data.get('language')

        book = Book.objects.create(
            title=title,
            author=author,
            published_date=published_date,
            book_image=book_image,
            language=language,
            owner=self.context['owner']
        )
        return book
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.book_image = validated_data.get('book_image', instance.book_image)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance
    

class BookDetailSerializer(serializers.ModelSerializer):
    books_owner = UserSerializer(read_only=True)
    books_category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    books_owner = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = "title", "author", "books_owner","book_image"