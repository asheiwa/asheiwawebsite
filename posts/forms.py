from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
	# publish = forms.DateField(widget=forms.SelectDateWidget)
	content = forms.CharField(widget=PagedownWidget)
	class Meta:
		model = Post
		fields = [
			'title',
			'category',
			'tag',
			'image',
			'content',
			'publish',
			'pin'
		]

class ContactForm(forms.Form):
	name = forms.CharField(label='Your Name')
	email = forms.EmailField(label='Email ( will not published )', widget=forms.EmailInput)
	subject = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)