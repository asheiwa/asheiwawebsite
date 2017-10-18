from urllib import quote_plus
from django import template

register = template.Library()

@register.filter
def split_tags(tags):
	if not tags:
		return ''
	return tags.split(', ')