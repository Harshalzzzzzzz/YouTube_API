from rest_framework import serializers
from .models import Videos


# Serializers to allow querysets and model instances converted to native Python datatypes to be rendered as JSON or XML.
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = "__all__"
