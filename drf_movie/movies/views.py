from django.db import models
from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """output movie list"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Avg(models.F('ratings__star'))
        )
        return movies

# class MovieListView(APIView):
#     """output movie list"""
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
#         ).annotate(
#             middle_star=models.Avg(models.F('ratings__star'))
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    """output movie list"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


# class MovieDetailView(APIView):
#     """output movie list"""
#     def get(self, request, pk):
#         movies = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movies)
#         return Response(serializer.data)


class ReviewCreateView(generics.CreateAPIView):
    """Add Review to Movie"""
    serializer_class = ReviewCreateSerializer


# class ReviewCreateView(APIView):
#     """Add Review to Movie"""
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)


class AddStarRatingView(generics.CreateAPIView):
    """Add Rating to Movie"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


# class AddStarRatingView(APIView):
#     """Add Rating to Movie"""
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """Output Actors list"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """Output Actors details"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
