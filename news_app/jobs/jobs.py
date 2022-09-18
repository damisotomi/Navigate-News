import requests
from pprint import pprint
from news_app.models import Comment, News
from django.db import transaction
from django.shortcuts import render


def schedule_api():

    max_item_id = News.objects.filter(
        item_id__isnull=False).order_by('-item_id')[0]
    max_item_id = int(max_item_id.item_id)

    last_news_items_id = requests.get(
        "https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty").json()

    pprint(last_news_items_id)

    while last_news_items_id > max_item_id:
        link = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(
            max_item_id+1)

        id_response = requests.get(link).json()
        
        title_check= id_response.get('title', None)

        if not title_check:
            max_item_id+=1
            continue

        if id_response['id'] in list(News.objects.values_list(flat=True)):
            max_item_id+=1
            continue

        if News.objects.filter(item_id=id_response['id']):
            max_item_id+=1
            continue

        if id_response['type'] == 'comment' or id_response['type'] is None:
            max_item_id += 1
            pprint(max_item_id)
            continue



        else:
            with transaction.atomic():
                news = News()
                news.item_id = id_response['id']
                news.author = id_response.get('by', None)
                news.descendants = id_response.get('descendants', None)
                news.score = id_response.get('score', None)
                news.title = id_response.get('title', None)
                news.type = id_response['type']
                news.url = id_response.get('url', None)
                news.save()

                kids = id_response.get('kids', None)
                if kids:
                    for comment_id in id_response['kids'][0:10]:
                        link = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty".format(
                            comment_id)
                        comment_response = requests.get(link).json()
                        comment = Comment()
                        comment.item_id = comment_response['id']
                        comment.author = comment_response.get('by', None)
                        comment.comment = comment_response.get('text', None)
                        comment.type = comment_response['type']
                        comment.news = news
                        comment.save()
            max_item_id += 1
            pprint(max_item_id)