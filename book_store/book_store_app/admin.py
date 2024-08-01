from django.contrib import admin
from .models import Book,BookSpecifications,Profile
# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'genre', 'price', 'quantity')



@admin.register(BookSpecifications)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('book_id','book_code','publisher','publish_date','pages','description')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user','gender','address','phone_number')

