from rest_framework.response import Response
from rest_framework.decorators import api_view
from hackapp.models import User, Hackathon
from hackapp.serializers import UserSerializer, HackathonSerializer

@api_view(['GET'])
def list(request):
    hackathons = Hackathon.objects.all()
    serializer = HackathonSerializer(hackathons, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create(request):
    serializer = HackathonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print(serializer.data)
    return Response("Item Not Added", 400)

@api_view(['PUT'])
def update(request, id):
    hackathon = Hackathon.objects.get(id=id)
    serializer = HackathonSerializer(hackathon, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response("Item not Updated")

@api_view(['DELETE'])
def delete(request, id):
    hackathon = Hackathon.objects.get(id=id)
    hackathon.delete()
    return Response("Item Deleted")
