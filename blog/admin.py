from django.contrib import admin

from blog.models import Blog


# Register your models here.

# admin.site.register(Student)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'image', 'created_at', 'is_published',)
