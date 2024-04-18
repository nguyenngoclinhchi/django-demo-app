from rest_framework import generics
from django.shortcuts import get_object_or_404

class ListCreateAPIViewBase(generics.ListCreateAPIView):
    serializer_class = None
    model_class = None

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):
        return self.serializer_class

class RetrieveUpdateDestroyAPIViewBase(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = None
    model_class = None

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_lookup_field(self):
        if 'slug' in self.kwargs:
            return 'slug'
        elif 'id' in self.kwargs:
            return 'id'
        else:
            return None

    def get_object(self):
        lookup_field = self.get_lookup_field()
        if lookup_field is None:
            return None
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, **{lookup_field: self.kwargs[lookup_field]})
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        return self.serializer_class