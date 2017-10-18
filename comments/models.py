from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils.safestring import mark_safe
from markdown_deux import markdown

# Create your models here.
class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager, self).filter(parent=None)

	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = instance.id
		qs = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
		return qs


class Comment(models.Model):
	# user      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=100) 

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	parent = models.ForeignKey("self", null=True, blank=True)
	
	content   = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.name)

	def children(self): # replies
		return Comment.objects.filter(parent=self)

	def get_markdown(self):
		return mark_safe( markdown(self.content) )

	def get_test(self):
		tst = 'this is the test'
		return tst


	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True