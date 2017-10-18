from __future__ import unicode_literals
import re

from django.conf import settings
import settings as st
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from datetime import datetime
from django.contrib.contenttypes.models import ContentType

from django.utils.safestring import mark_safe
from markdown_deux import markdown

# from pygments import highlight
# from pygments.lexers import PythonLexer
# from pygments.formatters import HtmlFormatter

from comments.models import Comment

# Create your models here.
# MVC = MODEL VIEW CONTROLLER

class PostManager(models.Manager):
	"""docstring for ClassName"""
	def active(self, *arg, **kwargs):
		return super(PostManager, self).filter(publish=True) #.filter(created__lte=datetime(2017, 5, 20))

def upload_location(instance, filename):
	return '%s/%s' %(instance.slug, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)

	category = models.CharField(max_length=3, default='OTH', choices=st.category_choices)
	tag = models.CharField(max_length=300, blank=True)

	image =  models.ImageField(upload_to=upload_location,
							   null=True,
							   blank=True,
							   width_field='width_field',
							   height_field='height_field')
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)
	content = models.TextField()
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified = models.DateTimeField(auto_now=True, auto_now_add=False)
	publish = models.BooleanField(default=False)
	pin = models.BooleanField(default=False)

	objects = PostManager()

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={'slug':self.slug})
		# return '/posts/%s/' % self.id

	def get_markdown(self):
		return mark_safe( markdown(self.content) )
		# return get_pygments(markdown(self.content))
		# return markdown(self.content)

	@property
	def comments(self):
		qs = Comment.objects.filter_by_instance(self)
		return qs

	@property
	def get_content_type(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return content_type
	

	class Meta:
		ordering = ['-created' ] #, '-modified']

def create_slug(instance, new_slug=None):
	slug = slugify( instance.title )
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		new_slug = '%s-%s' %( slug, qs.first().id )
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)

# def get_pygments(code):
# 	return highlight(code, PythonLexer(), HtmlFormatter())


