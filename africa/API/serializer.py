from rest_framework import serializers, renderers
from .models import *


class stove_serializer(serializers.ModelSerializer):
    class Meta:
        sensor_id = serializers.IntegerField()
        date = serializers.DateField()
        temperature = serializers.FloatField()


fields = ['number', 'date', 'amount_of_stoves', 'average_number_of_hours']

serializer_obj = stove_serializer(instance=fields, many=True)
# Рендерим данные в json
json_render_for_our_data = renderers.JSONRenderer()
data_in_json = json_render_for_our_data.render(serializer_obj.data)
