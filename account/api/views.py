from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from account.api.serializers import RegistrationSerializer,StartupSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from account.models import Startup

# Url: https://<your-domain>/api/register

@api_view(['POST',])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def userregister(request):
    print("hello")
    print("hello",request.method)
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        print("hiiii")
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            print("valid")
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['name'] = account.name
            data['contact_number'] = account.contact_number

            token = Token.objects.get(user=account).key

            data['token'] = token

        else:
            data = serializer.errors

        return Response(data)

@csrf_exempt
@api_view(['POST','GET','PUT','DELETE'])
@authentication_classes([])
@permission_classes([])
def Startup_api(request,id=None):
    if request.method=="GET":
        if id is None:
            data=Startup.objects.all()
            serializer=StartupSerializer(data,many=True)
            return Response(serializer.data)

        else:
            data=Startup.objects.filter(pk=id)
            serializer=StartupSerializer(data,many=True)
            return Response(serializer.data)


    if request.method=='POST':
        serializer=StartupSerializer(data=request.data)
       # print(serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg','DATA CREATED'})
        return Response(serializer.errors)

    if request.method=='PUT':
        data=Startup.objects.get(pk=id)
        serializer=StartupSerializer(data,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg','Data Updated'})
        return Response(serializer.errors)

    if request.method=='DELETE':
        data=Startup.objects.get(pk=id)
        data.delete()
        return Response({'msg':'data deleted'})
