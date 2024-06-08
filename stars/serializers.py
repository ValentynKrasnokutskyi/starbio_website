from rest_framework import serializers
from .models import Stars


# Serializer for the Stars model
class StarsSerializer(serializers.ModelSerializer):
    # The author field will be automatically populated with the current user
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Stars  # Specifies that this serializer is for the Stars model
        fields = "__all__"  # Includes all fields of the model in the serializer


# class StarsSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Stars.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance
