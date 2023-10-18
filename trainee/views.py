from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .serializers import TraineeSerializer
from .models import Trainee


# Create your views here.
@api_view(['GET', 'PATCH', 'DELETE'])
@login_required()
def get_update_delete_trainee(req, pk):
    try:
        trainee = Trainee.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({'status': False, 'data': {}, 'messages': ['Cannot find a trainee with the specified id!']},
                        status=status.HTTP_404_NOT_FOUND)

    if req.method == 'GET':
            serialized_data = TraineeSerializer(trainee)
            return Response({'status': True, 'data': serialized_data.data, 'messages': []}, status=status.HTTP_200_OK)

    if req.method == 'PATCH':
        serialized_data = TraineeSerializer(trainee, data=req.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'status': True, 'data': serialized_data.data, 'messages': []},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': False, 'data': serialized_data.errors, 'messages': serialized_data.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    if req.method == 'DELETE':
        trainee.delete()
        return Response({'status': True, 'data': {}, 'messages': ['Trainee deleted successfully.']},
                        status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required()
def list_add_trainees(req):
    if req.method == 'GET':
        data = Trainee.objects.all()
        serialized_data = TraineeSerializer(data, many=True)
        return Response({'status': True, 'data': serialized_data.data, 'messages': []}, status=status.HTTP_200_OK)

    serialized_data = TraineeSerializer(data=req.data)
    if serialized_data.is_valid():
        trainee = serialized_data.save()
        return Response({'status': True, 'data': TraineeSerializer(trainee).data, 'messages': []},
                        status=status.HTTP_201_CREATED)

    return Response({'status': True, 'data': serialized_data.data, 'messages': serialized_data.errors},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
# @login_required()
def update_trainee(req, pk):
    trainee = Trainee.objects.get(id=pk)
    serialized_data = TraineeSerializer(trainee, data=req.data)

    if serialized_data.is_valid():
        serialized_data.save()
        return Response({'status': True, 'data': serialized_data.data, 'messages': []}, status=status.HTTP_200_OK)
    else:
        return Response({'status': False, 'data': serialized_data.errors, 'messages': serialized_data.errors},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required()
def search_trainees(req):
    search_term = req.query_params.get('q', '')
    trainees = Trainee.objects.filter(name__icontains=search_term)
    serialized_data = TraineeSerializer(trainees, many=True)
    return Response({'status': True, 'data': serialized_data.data, 'messages': []}, status=status.HTTP_200_OK)
