from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ['id','title','category','created','image','publish','pin']
	prepopulated_fields = {'slug':('title',) }
	list_display_links = ['title']
	list_filter = ['created','modified']
	search_fields = ['title','content','category']
	list_editable = ['publish','pin']

	class Meta:
		model = Post
			

admin.site.register(Post, PostModelAdmin)