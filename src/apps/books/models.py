from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# Create your models here.
class Catregory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.ForeignKey(Catregory, on_delete=models.CASCADE, blank=True, null=True, related_name='books_category')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_owner')
    published_date = models.DateField(null=True, blank=True)
    book_image = models.ImageField(blank=True, null=True)
    language = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)


    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
class BookTransaction(models.Model):
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_transactions')
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lent_books')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('reviewer', 'book') 


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment_vote(models.Model):
    choice_field= (
        ('upvote','Upvote'),
        ('downvote','Downvote')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_votes')
    vote = models.CharField(max_length=10, choices=choice_field)

    class Meta:
        unique_together = ('user', 'comment')
