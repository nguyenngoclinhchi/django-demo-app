from django.contrib.auth.decorators import permission_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Data
from .serializer import DataSerializer

# START OUR CRUD OPERATIONS
# Create your views here.

@api_view(['GET', 'POST'])
@permission_required('healthapp.data_list')
def data_list(request):
    if request.method == "GET":
        app = Data.objects.all()
        serializer = DataSerializer(app, many=True)
        # return JsonResponse(
        #     {'healthapp': serializer.data}, safe=False
        # )
        return Response(
            {'healthapp': serializer.data}, status=status.HTTP_200_OK
        )
    if request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def drink_detail(request, id):
    try: 
        data = Data.objects.get(pk=id)
    except Data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = DataSerializer(data)
        return Response(
            {'healthapp': serializer.data}, status=status.HTTP_200_OK
        )
    elif request.method == "PUT":
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'healthapp': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
