from dataclasses import field
from rest_framework import serializers
from .models import Comment, News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'author', 'title', 'type', 'text',
                  'url']

    def create(self, validated_data):
        classification = self.context['classification']
        return News.objects.create(classification=classification, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['id','author','comment']

    def create(self, validated_data):
        news_id=self.context['news_id']
        classification=self.context['classification']
        return Comment.objects.create(news_id=news_id,classification=classification, **validated_data)