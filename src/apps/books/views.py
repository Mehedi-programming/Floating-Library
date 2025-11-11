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
        serializer = BookCreateUpdateSerializer(data=request.data, context={'request':request,  'owner': request.user})
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        bookSerializer = BookDetailSerializer(book)
        return Response({"message": "Book created successfully", "data": bookSerializer.data}, status=status.HTTP_201_CREATED)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
        books = Book.objects.filter(Q(title__icontains=query) |
                                    Q(author__icontains=query) |
                                    Q(category__name__icontains=query)).distinct()
    else:
        books = Book.objects.all()  
    if not books.exists(): 
        return Response({"message": "Books not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = BookListSerializer(books, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)

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
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def borrowed_books(request):
        transactions = BookTransaction.objects.filter(borrower=request.user)
        books = [transaction.book for transaction in transactions]
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def lent_books(request):
        transactions = BookTransaction.objects.filter(lender=request.user)
        books = [transaction.book for transaction in transactions]
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user_books(request):
        books = Book.objects.filter(owner=request.user)
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_comment(request, book_id):
    post = get_object_or_404(Book, pk=book_id)
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user, post=post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def edit_comment(requset, comment_id):
        comment = get_object_or_404(Comment, pk=id)
        if comment.user != requset.user:
                return Response({"error":"You can't edit the comment."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=requset.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 

      
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def  delete_comment(request,id):
    comment = get_object_or_404(Comment, pk=id)
    if comment.user != request.user:
        return Response({"error":"You can't delete the comment."}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({"message":"Comment deleted successfully."}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def  votes_comment(request, comment_id, action):
    comment = get_object_or_404(Comment, pk=comment_id)
    if action == 'upvotes':
        comment.upvotes += 1
        comment.save(update_fields=['upvotes'])
    elif action == 'downvotes':
        comment.downvotes += 1
        comment.save(update_fields=['downvotes'])
    else:
        return Response({"error":"Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)


































@api_view(["GET"])
def popular_books(request):
        books = Book.objects.annotate(total_votes=sum('book_reviews__votes'))>10
        serializer = BookListSerializer(books, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)




@api_view(["GET"])
def borrow_request(request):
       ...
       




   
    

        

       
