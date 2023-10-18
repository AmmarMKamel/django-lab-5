from rest_framework import serializers
from .models import Track, Trainee


class TraineeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    birth_date = serializers.DateField(required=False)
    track_id = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all(), required=False)

    def create(self, validated_data):
        return Trainee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.track_id = validated_data.get('track_id', instance.track_id)
        instance.save()
        return instance
