from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Catregory)
admin.site.register(Book)
admin.site.register(BorrowRequest)
admin.site.register(BookReview)
admin.site.register(Comment)
admin.site.register(Comment_vote)
admin.site.register(WishList)