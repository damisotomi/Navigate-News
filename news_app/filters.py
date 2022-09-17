from django_filters.rest_framework import FilterSet
from django_filters import FilterSet as FS
from .models import News,Comment


class NewsFilter(FilterSet):
    '''For the Api'''
    class Meta:
        model = News
        fields = {
            'author': ['iexact'],
            'title': ['icontains'],
            'classification':['icontains'],
            'type':['exact']
        }


class NewsListFilter(FS):
    '''For the List view'''
    class Meta:
        model = News
        fields = {
            'author':['icontains'],
            'title':['icontains'],
            'type':['exact']

        }


class CommentFilter(FilterSet):
    '''For the Api'''
    class Meta:
        model = Comment
        fields = {
            'author': ['icontains'],
            'classification':['icontains'],
        }
