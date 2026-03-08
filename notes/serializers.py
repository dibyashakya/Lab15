from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=100,
        error_messages={'required': 'Title is required', 'blank': 'Title is required'}
    )
    description = serializers.CharField(
        error_messages={'required': 'Description is required', 'blank': 'Description is required'}
    )
    created_at = serializers.DateTimeField(read_only=True)

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance