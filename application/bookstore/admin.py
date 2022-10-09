from django.contrib import admin

from bookstore.models import Category, SubCategory, PaperBook, BookReview, Order

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PaperBook)
admin.site.register(BookReview)
admin.site.register(Order)
