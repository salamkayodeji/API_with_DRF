from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .tokens import create_jwt_pair_for_user
from rest_framework.request import Request
from django.contrib.auth import authenticate



class LoginView(APIView):
    """ This is used to authenticate user """

    permission_classes = []

    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)

#
class TodoViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given Todo takes params pk.

    list:
    Return a list of all the existing Todo.

    create:
    Create a new Tudo instance.
    
    update:
    Update a given Todo instance
    
    delete:
    Delete a given Todo instance

    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    
class EventViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given Event takes params pk.

    list:
    Return a list of all the existing Events.

    create:
    Create a new Event instance.
    
    update:
    Update a given Event instance
    
    delete:
    Delete a given Event instance

    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
  
@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def Duplicate_Todo(request, pk):
    '''
    It duplicate a give Todo and all events that foreign key to the and returns returns the Todo and Events 
    created.

            Parameters:
                    pk (int): The id of the Todo to duplicated

            Returns:
                    response (dict): Dictionary of with the created Todo and Events
    '''

    todo = Todo.objects.get(pk=pk)
    events = Event.objects.filter(todo= todo) 
    new_todo = Todo.objects.create(name = todo.name, user = request.user)
    for i in events:
        new_event = Event.objects.create(todo = new_todo,
                                          complete = i.complete,
                                          event_name = i.event_name,
                                          date_created = i.date_created,
                                          last_modified = i.last_modified)
        new_event.save()
    new_event = Event.objects.filter(todo = new_todo)
    
    serializer = TodoSerializer(new_todo)
    event_serializer = EventSerializer(new_event, many = True)    
    return Response({
            "**Todo**": serializer.data,
            "**Event**": event_serializer.data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Duplicate_Event(request, pk):
    '''
    It duplicate a give Event and returns returns the newly created Event 
    created.

            Parameters:
                    pk (int): The id of the Event to duplicated

            Returns:
                    response (dict): Dictionary of with the created Events created
    '''

    event = get_object_or_404(Event, id= pk)
    new_event = Event.objects.create(todo = event.todo,
                                    complete = event.complete,
                                    event_name = event.event_name,
                                    date_created = event.date_created,
                                    last_modified = event.last_modified)
    new_event.save()
    serializer = EventSerializer(new_event, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def get_events(request, pk):
    '''
    Returns a list of all events where todo == pk.

            Parameters:
                    pk (int): The id of the Todo 

            Returns:
                    response (dict): Dictionary of the events returned
    '''

    todo = get_object_or_404(Todo, id= pk)
    event = Event.objects.filter(todo = todo)
    serializer = EventSerializer(event, many=True)
    if serializer:
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_events_todo(request, pk):
    '''
    Returns a Todos and a list of events with relationship with the Todo.

            Parameters:
                    pk (int): The id of the Todo 

            Returns:
                    response (dict): Dictionary with a Todo and a list of events
    '''

    todo = get_object_or_404(Todo, id= pk)
    event = Event.objects.filter(todo = todo)
    serializer_event = EventSerializer(event, many=True)
    serializer_todo = TodoSerializer(todo)
    return Response({
            "**Todo**": serializer_todo.data,
            "**Event**": serializer_event.data
        }, status=status.HTTP_200_OK)


@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def Get_Todo_Event(request):
    '''
    Returns a list of all Todos and a list of all events.


            Returns:
                    response (dict): Dictionary with all Todo and all events
    '''

    todo = Todo.objects.all()
    events = Event.objects.all()
    todo_serializer = TodoSerializer(todo, many = True)    
    event_serializer = EventSerializer(events, many = True)  
    return Response({
            "**Todo**": todo_serializer.data,
            "**Event**": event_serializer.data
        }, status=status.HTTP_200_OK)
    
"""
    todo_data = {}
    todo_data = todo_serializer.data
    event_data = {}
    event_data = event_serializer.data
    data = {}
    num = 1
    while num < len(todo_data):
        new_list = []
        for i in range(1, len(event_data)):
            if todo_data[num]["id"] == event_data[i]["todo"]:
                new_list.append(event_data)
        data[todo_data[num]["id"]] = new_list
        num += 1
    print(data)
    return Response(data)
"""
    
    

    
