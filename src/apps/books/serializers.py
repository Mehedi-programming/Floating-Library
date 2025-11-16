# from rest_framework import serializers
# from .models import *


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username"]


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Catregory
#         fields = ['id', "name"]


# class BookCreateUpdateSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(write_only=True, required=False)  
#     owner = UserSerializer(read_only=True)     
#     category = CategorySerializer(read_only=True)


#     class Meta:
#         model = Book
#         fields = ["title", "author", "category_name", "published_date", "book_image", "language", "owner","category"]

#     def create(self, validated_data):
#         category_name = validated_data.pop("category_name", None)
#         owner = self.context['request']
#         book = Book.objects.create(owner=owner, **validated_data)
#         if category_name:
#             category_obj, _ = Catregory.objects.get_or_create(
#                 name=category_name.strip().lower()
#             )
#             book.category = category_obj
#             book.save()
#         return book
    
    
#     def update(self, instance, validated_data):
#         category = validated_data.pop('category_name', None)
#         instance.title = validated_data.get('title', instance.title)
#         instance.author = validated_data.get('author', instance.author)
#         instance.published_date = validated_data.get('published_date', instance.published_date)
#         instance.book_image = validated_data.get('book_image', instance.book_image)
#         instance.language = validated_data.get('language', instance.language)
#         category_obj, _ = Catregory.objects.get_or_create(name=category.strip().lower())
#         instance.category = category_obj
#         instance.save()
#         return instance
    

# class BookDetailSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(read_only=True)
#     category = CategorySerializer(read_only=True)

#     class Meta:
#         model = Book
#         fields = fields = [
#             'id', 'title', 'author', 'published_date',
#             'book_image', 'language', 'created_at', 'updated_at',
#             'slug', 'category', 'owner'
#         ]

#     def get_category(self, obj):
#         if obj.category:
#             return {"name": obj.category.name}
#         return None


# class BookListSerializer(serializers.ModelSerializer):
#     books_owner = UserSerializer(read_only=True)

#     class Meta:
#         model = Book
#         fields = ["title", "author", "books_owner", "book_image"]


from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catregory
        fields = ['id', "name"]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=False)  
    owner = UserSerializer(read_only=True)       

    class Meta:
        model = Book
        fields = [
            "title", "author", "category_name",
            "published_date", "book_image",
            "language", "owner", "category"
        ]

    def create(self, validated_data):
        category = validated_data.pop("category_name", None)
        owner = self.context['request'].user
        book = Book.objects.create(owner=owner, **validated_data)

        if category:
            category_obj, _ = Catregory.objects.get_or_create(
                name=category.strip().lower()
            )
            book.category = category_obj
            book.save()
        return book

    def update(self, instance, validated_data):
        category = validated_data.pop('category_name', None)
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.book_image = validated_data.get('book_image', instance.book_image)
        instance.language = validated_data.get('language', instance.language)

        if category:
            category_obj, _ = Catregory.objects.get_or_create(
                name=category.strip().lower()
            )
            instance.category = category_obj

        instance.save()
        return instance


class BookDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'published_date',
            'book_image', 'language', 'created_at', 'updated_at',
            'slug', 'category', 'owner'
        ]


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["id", "title", "author",  "book_image"]

    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField(method_name="replys")
    
    def replys(self, obj):   
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data
    
    class Meta:
        model = Comment
        fields = ["id", "user", "content", "parent", "replies", "created_at", "upvotes", "downvotes"]
