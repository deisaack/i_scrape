from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'shortcode', 'likes', 'comments', 'timestamp']
    list_display_links = ['id', 'shortcode']
    list_filter = ['tag']

admin.site.register(Post, PostAdmin)

