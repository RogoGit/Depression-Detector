import copy

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

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
