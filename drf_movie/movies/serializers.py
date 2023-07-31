from rest_framework import serializers

from .models import Movie, Review


class MovieListSerializer(serializers.ModelSerializer):
    """Movie list"""

    class Meta:
        model = Movie
        fields = ("title", "tagline", "category")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """add Review"""
    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Output Review"""
    class Meta:
        model = Review
        exclude = ("draft", )


class MovieDetailSerializer(serializers.ModelSerializer):
    """Full Movie"""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewCreateSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )
