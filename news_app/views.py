import requests
from pprint import pprint
from django.shortcuts import render
from django.db import transaction
from django.views import generic
from django.urls import reverse_lazy
from django_filters.views import FilterView
from .models import Comment, News
from .serializers import NewsSerializer,CommentSerializer
from .filters import NewsFilter,NewsListFilter,CommentFilter 
from .pagination import DefaultPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

def index(request):
    return render(request, 'index.html')

class NewsList(FilterView):

    queryset = News.objects.prefetch_related(
    'comments').order_by('-id').all()

    context_object_name = 'news_queryset'
    paginate_by = 15
    template_name = 'news_list.html'

    filterset_class=NewsListFilter


class NewsDetailView(generic.DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'


class CommentCreateView(generic.CreateView):
    model=Comment
    template_name='comment_form.html'
    fields=['author','comment']
    
    def form_valid(self, form):
        form.instance.news=News(id=self.kwargs['pk'])
        form.instance.classification='User Upload'
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('news_detail',kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs['pk']
        news_queyset=News.objects.filter(id=self.kwargs['pk'])[0]
        context['title']=news_queyset.title
        return context


# API VIEW
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsFilter
    search_fields = ['author', 'title']
    ordering_fields = ['author', 'title', 'last_update']
    pagination_class = DefaultPagination

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance.classification == "HackerNews":
            return Response({"error": "This News item cannot be Edited. It comes directly from Hacker news"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classification == "HackerNews":
            return Response({"error": "This News item cannot be deleted. It comes directly from Hacker news"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        return {'classification': 'Api'}


class CommentViewSet(ModelViewSet):
    serializer_class=CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['author']
    ordering_fields = ['author']
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Comment.objects.filter(news_id=self.kwargs['news_pk'])
    
    def get_serializer_context(self):
        return {'news_id':self.kwargs['news_pk'],'classification':'Api'}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classification == "Api":
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "This Comment Cannot cannot be deleted. Only comments added via an API post request can be deleted"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if instance.classification == "Api":
            self.perform_update(serializer)
        else:
            return Response({"error": "This Comment cannot be Edited. Only comments  added via an API POST request can be edited"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

# Used to load the db with the first 50 news. Only to be used when the db is completely empty. 

# def load_db(request):
#     last_news_item=requests.get("https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty").json()
#     count=0
#     while count<50:
#         link="https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(last_news_item)
#         id_response = requests.get(link).json()
#         if id_response['type']=='comment':
#             last_news_item-=1
#             continue
#         else:
#             with transaction.atomic():
#                 news = News()
#                 news.item_id = id_response['id']
#                 news.author = id_response.get('by', None)
#                 news.descendants = id_response.get('descendants', None)
#                 news.score = id_response.get('score', None)
#                 news.title = id_response.get('title', None)
#                 news.type = id_response['type']
#                 news.url = id_response.get('url', None)
#                 news.save()

#                 kids = id_response.get('kids', None)
#                 if kids:
#                     for comment_id in id_response['kids'][0:10]:
#                         link = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(
#                             comment_id)
#                         comment_response = requests.get(link).json()
#                         comment = Comment()
#                         comment.item_id = comment_response['id']
#                         comment.author = comment_response.get('by', None)
#                         comment.comment = comment_response.get('text', None)
#                         comment.type = comment_response['type']
#                         comment.news = news
#                         comment.save()
#             last_news_item-=1
#             count+=1
#     return render(request,'test.html')

