from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count, Avg, Sum, Max, Min



# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def book_create(request):
        serializer = BookCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save(owner=request.user)
        bookSerializer = BookDetailSerializer(book)
        return Response({"message": "Book created successfully", "data": bookSerializer.data}, status=status.HTTP_201_CREATED)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def book_update(request, book_id):
        book = get_object_or_404(Book, id=book_id, owner=request.user)
        serializer = BookCreateUpdateSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        book_data = serializer.save(owner=request.user)
        bookSerializer = BookDetailSerializer(book_data)
        return Response({"message": "Book updated successfully", "data": bookSerializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def book_details(request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookDetailSerializer(book)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def book_list(request):
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def book_search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Book.objects.filter(Q(title__icontains=query) |
                                    Q(author__icontains=query) |
                                    Q(category__name__icontains=query)).distinct()
    else:
        posts = Book.objects.datetimes('created_at', 'year')
    if not Book.exists():
        return Response({"message": "No posts found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookListSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def book_delete(request, book_id):
        book = get_object_or_404(Book, id=book_id, owner=request.user)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_list(request):
        categories = Catregory.objects.all()
        serializers = CategorySerializer(categories, many=True)
        return Response({"data": serializers.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def books_by_category(request, category_id):
        category = get_object_or_404(Catregory, id=category_id)
        books = Book.objects.filter(category=category)
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def updated_books(request):
        books = Book.objects.datetimes('created_at', 'month')
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

@api_view(["GET"])
def popular_books(request):
        books = Book.objects.annotate(total_votes=sum('book_reviews__votes'))>10
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def user_books(request):
        books = Book.objects.filter(owner=request.user)
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def borrowed_books(request):
        transactions = BookTransaction.objects.filter(borrower=request.user)
        books = [transaction.book for transaction in transactions]
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def borrow_request(request):
       ...
       


@api_view(["GET"])
def lent_books(request):
        transactions = BookTransaction.objects.filter(lender=request.user)
        books = [transaction.book for transaction in transactions]
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

   
    

        



               