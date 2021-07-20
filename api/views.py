from .models import Videos
from ._serialize import VideoSerializer

# Rest FrameWork
from rest_framework import generics
from rest_framework.pagination import CursorPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.core.paginator import Paginator
from django.http import JsonResponse


# Pagination to control how many objects per page are returned.
class ResultsPagination(CursorPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


# Generic class-based view
class VideoItems(generics.ListAPIView):
    search_fields = ["title", "description"]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ["channel_id", "channel_title"]
    ordering = "-published_at"
    queryset = Videos.objects.all()
    # VideoSerializer converts Video model's instances into representations such as json
    serializer_class = VideoSerializer
    pagination_class = ResultsPagination


def show(request):
    try:
        query_title = request.GET.get("q")
        page_number = int(request.GET.get("page"))
        search_results = Videos.objects.filter(
            title__icontains=query_title if query_title is not None else "",
            description__contains=query_title if query_title is not None else "",
        ).order_by("-published_at")
        paginator = Paginator(search_results, 25)
        page_obj = paginator.get_page(page_number)
        serialized_results = VideoSerializer(page_obj.object_list, many=True)
        return JsonResponse({"result": serialized_results.data, "total_page": paginator.num_pages})

    except Exception as e:
        return JsonResponse({"success": "failed", "result": e})
