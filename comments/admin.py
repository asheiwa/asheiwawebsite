from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):
	list_display = ['id','name','email','timestamp', 'content']
	list_display_links = ['name']
	list_filter = ['email','name']
	search_fields = ['name','content']

admin.site.register(Comment, CommentModelAdmin)