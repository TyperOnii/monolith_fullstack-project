from rest_framework import serializers

class ExtendedModelsSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True