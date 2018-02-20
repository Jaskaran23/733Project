from API.models import Page
from rest_framework import serializers, generics

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'


class PageList(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

