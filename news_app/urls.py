from pprint import pprint
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('api/news', views.NewsViewSet, basename='news')
# pprint(router.urls)

news_router=routers.NestedDefaultRouter(router,'api/news',lookup='news')
news_router.register('comments',views.CommentViewSet,basename='news-comment')
# pprint(news_router.urls)

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.NewsList.as_view(), name='news'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/addcomment/', views.CommentCreateView.as_view(), name='comment_form'), 
    # path('load/', views.load_db, name='load_db'),    
]+router.urls+news_router.urls
