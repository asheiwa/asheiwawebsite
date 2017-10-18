from django import forms
from .models import Comment
from pagedown.widgets import PagedownWidget

# class CommentForm(forms.Form):
# 	content_type = forms.CharField(widget=forms.HiddenInput)
# 	object_id = forms.IntegerField(widget=forms.HiddenInput)
# 	# parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
# 	name = forms.CharField(label='Name', widget=forms.TextInput)
# 	email = forms.EmailField(label='Email ( will not published )')
# 	content = forms.CharField(label='', widget=forms.Textarea)




class CommentForm(forms.Form):
	# publish = forms.DateField(widget=forms.SelectDateWidget)
	# content = forms.CharField(label='', widget=PagedownWidget)
	content = forms.CharField(label='', widget=forms.Textarea)
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	name = forms.CharField(label='Name', widget=forms.TextInput)
	email = forms.EmailField(label='Email ( will not published )')
	class Meta:
		model = Comment
		fields = [
			'content'
		]