import copy
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from .dd_integration import get_depression
from .models import Model
from .serializers import ModelSerializer


# Create your views here.
class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

    def create(self, request, *args, **kwargs):
        data = copy.deepcopy(request.data)
        data['depression_detection_result'] = get_depression(data['text'])['label']

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        headers = self.get_success_headers(serializer.data)

        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
        all_models = Model.objects.filter(date_of_birth__year=date_of_birth.year)

        all_sum = 0
        depressive_sum = 0
        non_depressive_sum = 0

        for x in all_models:
            all_sum += 1
            if x.depression_detection_result == 'DEPRESSIVE':
                depressive_sum += 1
            if x.depression_detection_result == 'NON-DEPRESSIVE':
                non_depressive_sum += 1

        data = copy.deepcopy(serializer.data)
        data['depressive_text_amount'] = depressive_sum / all_sum
        data['non_depressive_text_amount'] = non_depressive_sum / all_sum

        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
