from .models import Videos
from ._serialize import VideoSerializer

# Rest FrameWork
from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend



class ResultsPagination(CursorPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class VideoItems(generics.ListAPIView):
    search_fields = ["title", "description"]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ["channel_id", "channel_title"]
    ordering = "-published_at"
    queryset = Videos.objects.all()
    serializer_class = VideoSerializer
    pagination_class = ResultsPagination

