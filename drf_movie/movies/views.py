from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer
from .service import get_client_ip


class MovieListView(APIView):
    """output movie list"""
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Avg(models.F('ratings__star'))
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """output movie list"""
    def get(self, request, pk):
        movies = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movies)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Add Review to Movie"""
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Add Rating to Movie"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


