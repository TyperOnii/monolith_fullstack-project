from rest_framework import serializers
from django.shortcuts import get_object_or_404

class ExtendedModelsSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def get_from_url(self, lookup_field):
        """Метод получения данных из url"""
        assert 'view' in self.context, (
            'No view context in "%s". '
            'Check parameter context on function calling.' % self.__class__.__name__
        )
        assert self.context['view'].kwargs.get(lookup_field), (
            'Got no data from url in "%s".'
            'Check lookup field on function calling.'  % self.__class__.__name__
        )

        value = self.context['view'].kwargs.get(lookup_field)
        return value
    
    def get_object_from_url(self, model, lookup_field = 'pk', model_field = 'pk'):
        """Метод получения объекта из url по lookup_field и model_field"""
        obj_id = self.get_from_url(lookup_field)
        obj = get_object_or_404(
            queryset = model.objects.all(),
            **{model_field: obj_id}
        )

        return obj