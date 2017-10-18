from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

# from pygments import highlight
# from pygments.lexers import PythonLexer
# from pygments.formatters import HtmlFormatter
# from pygments.styles import get_style_by_name

from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm, ContactForm

# Create your views here.
def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key in form.cleaned_data:
			# print key, ':', form.cleaned_data.get(key)
		name = form.cleaned_data.get('name')
		email = form.cleaned_data.get('email')
		subject = form.cleaned_data.get('subject')
		message = form.cleaned_data.get('message')

		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'a5heiwa@yahoo.com']
		contact_message = '%s \n %s via %s' % (message, name, email)
		send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

		messages.success(request, 'Email sent. Thank you.')
		return HttpResponseRedirect('/contact/')

	post_pin = post_pin_all(auth=False)

	context = {
		'form': form,
		'post_pin':post_pin
	}
	return render(request, 'contact.html', context)

def gallery(request):
	post_pin = post_pin_all(auth=False)
	post_atw = Post.objects.filter(category='ATW').filter(publish=True)
	context = {
		'post_pin':post_pin,
		'post_atw':post_atw
	}
	return render(request, 'gallery.html', context)

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	queryset_list = Post.objects.active()
	tag_all = post_tag_all(queryset_list)

	post_pin = post_pin_all(auth=True)

	post_count = post_category_count(auth=True)

	recent_post = Post.objects.active()[:10]

	recent_comments = Comment.objects.all()[:10]

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		# message success
		messages.success(request, 'Successfully Created')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'title':'Create Post',
		'form': form,
		'post_count':post_count,
		'recent_post':recent_post,
		'tag_all':tag_all,
		'recent_comments':recent_comments,
		'post_pin':post_pin
	}
	return render(request, 'post_form.html', context)

def post_detail(request, slug): # retrieve
	instance = get_object_or_404(Post, slug=slug)

	if not instance.publish:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404

	queryset_list = Post.objects.active()
	tag_all = post_tag_all(queryset_list)

	post_pin = post_pin_all(auth=True)

	post_count = post_category_count(auth=True)

	recent_post = Post.objects.active()[:10]

	recent_comments = Comment.objects.all()[:10]

	initial_data = {
					"content_type":instance.get_content_type,
					"object_id":instance.id
					}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		name = form.cleaned_data.get("name")
		email = form.cleaned_data.get("email")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
															name = name,
															email = email,
															content_type = content_type,
															object_id = obj_id,
															content = content_data,
															parent = parent_obj
															)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	comments = instance.comments

	context = {
		'title':instance.title,
		'instance':instance,
		'post_count':post_count,
		'recent_post':recent_post,
		'tag_all':tag_all,
		'comments':comments,
		'comment_form':form,
		'recent_comments':recent_comments,
		'post_pin':post_pin
	}
	return render(request, 'post_detail.html', context)

def post_list(request): # list items
	queryset_list = Post.objects.active() #.order_by('-modified')
	auth = False
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
		auth = True

	tag_all = post_tag_all(queryset_list)

	category = request.GET.get('c', '')
	if category: queryset_list = Post.objects.active().filter(category=category)

	tag = request.GET.get('t','')
	if tag: queryset_list = Post.objects.active().filter(tag__icontains=tag)

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()

	post_pin = post_pin_all(auth)

	post_count = post_category_count(auth)

	recent_post = Post.objects.active()[:10]

	recent_comments = Comment.objects.all()[:10]

	paginator = Paginator(queryset_list, 5) # Show 5 contacts per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		'auth':auth,
		'object_list':queryset,
		'title':'Post List',
		'page_request_var':page_request_var,
		'post_count':post_count,
		'recent_post':recent_post,
		'tag_all':tag_all,
		'recent_comments':recent_comments,
		'post_pin':post_pin
	}
	return render(request, 'index.html', context)


def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	queryset_list = Post.objects.active()
	tag_all = post_tag_all(queryset_list)

	post_count = post_category_count(auth=True)

	recent_post = Post.objects.active()[:10]

	recent_comments = Comment.objects.all()[:10]

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, 'Saved')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'title':'Edit Post',
		'instance':instance,
		'form':form,
		'post_count':post_count,
		'recent_post':recent_post,
		'tag_all':tag_all,
		'recent_comments':recent_comments
	}

	return render(request, 'post_form.html', context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, 'Successfully deleted')
	return redirect('posts:list')

def post_category_count(auth=False):
	if auth:
		result = {  'ATW' : Post.objects.filter(category='ATW').count(),
					'PGT' : Post.objects.filter(category='PGT').count(),
					'RGN' : Post.objects.filter(category='RGN').count(),
					'SCT' : Post.objects.filter(category='SCT').count(),
					'MDL' : Post.objects.filter(category='MDL').count(),
					'TRL' : Post.objects.filter(category='TRL').count(),
					'OTH' : Post.objects.filter(category='OTH').count()
				}
	else:
		result = {  'ATW' : Post.objects.filter(category='ATW').filter(publish=True).count(),
					'PGT' : Post.objects.filter(category='PGT').filter(publish=True).count(),
					'RGN' : Post.objects.filter(category='RGN').filter(publish=True).count(),
					'SCT' : Post.objects.filter(category='SCT').filter(publish=True).count(),
					'MDL' : Post.objects.filter(category='MDL').filter(publish=True).count(),
					'TRL' : Post.objects.filter(category='TRL').filter(publish=True).count(),
					'OTH' : Post.objects.filter(category='OTH').filter(publish=True).count()
				}

	return result

def post_pin_all(auth=False):
	if auth:
		post_pin = Post.objects.filter(pin=True)
	else:
		post_pin = Post.objects.filter(pin=True).filter(publish=True)
	result = dict()
	for x in range(post_pin.count()):
		result[x] = post_pin[x]
	return result

def post_tag_all(queryset_list):
	tag_all = []
	for tag in set(queryset_list.values_list("tag", flat=True)):
		if not tag in tag_all:
			if not ', ' in tag and not tag in tag_all:
				tag_all.append(tag)
			else:
				for t in tag.split(', '):
					if not t in tag_all:
						tag_all.append(t)
	return tag_all

# def testPygments():

# 	code = '''
# class DateSelectorWidget(widgets.MultiWidget):
#     def __init__(self, attrs=None):
#         # create choices for days, months, years
#         # example below, the rest snipped for brevity.
#         years = [(year, year) for year in (2011, 2012, 2013)]
#         _widgets = (
#             widgets.Select(attrs=attrs, choices=days),
#             widgets.Select(attrs=attrs, choices=months),
#             widgets.Select(attrs=attrs, choices=years),
#         )
#         super(DateSelectorWidget, self).__init__(_widgets, attrs)
# 	'''
# 	style = get_style_by_name('colorful')
# 	return highlight(code, PythonLexer(), HtmlFormatter(style=style))