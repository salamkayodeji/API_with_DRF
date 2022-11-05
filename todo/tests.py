from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from datetime import datetime, timedelta, date
from .models import *
from .serializers import *
import json


User = get_user_model()


# Create your tests here.

class EventListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("event-list")
        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        self.user = user

        
    def authenticate(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "john",
                "password": "johnpassword",
            },
        )
        token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
    def test_create_events(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        sample_data = {"todo": 1, "event_name": "Sample Items to do now", "complete":True,  "date_created":date.today(), "last_modified":date.today()}
        response = self.client.post(reverse("event-list"), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_events(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        # get API response
        response = self.client.get(self.url)
        # get data from db
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_valid_single_event(self):
        self.authenticate()
        self.todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        self.todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        event1 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= self.todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= self.todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())

        response = self.client.get(
        reverse("event-detail", kwargs={'pk': event1.pk}))
        event = Event.objects.get(pk=event1.pk)
        serializer = EventSerializer(event)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_event(self):
        self.authenticate()
        response = self.client.get(
        reverse("event-detail", kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_valid_delete_event(self):
        self.authenticate()
        self.todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        self.todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        event1 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= self.todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= self.todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        response = self.client.delete(
        reverse('todo-detail', kwargs={'pk': event2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_valid_update_event(self):
        self.authenticate()
        self.todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        self.todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        event1 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= self.todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= self.todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        updatedata = {"todo": 2, "event_name": "This Item is updated", "complete":True, "date_created":date.today() - timedelta(days = 1), "last_modified":date.today()}
        response = self.client.put(
        reverse('event-detail', kwargs={'pk': event1.pk}), updatedata)
        event = Event.objects.get(pk=event1.pk)
        serializer = EventSerializer(event)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("todo-list")
        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        self.user = user

        
    def authenticate(self):

        response = self.client.post(
            reverse("login"),
            {
                "username": "john",
                "password": "johnpassword",
            },
        )
        token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        
    def test_post_todo(self):
        self.authenticate()

        sample_data = {"user": 1, "name": "Sample Items to do", "timestamp":datetime.now()}
        response = self.client.post(reverse("todo-list"), sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_todos(self):
        self.authenticate()
        Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        # get API response
        response = self.client.get(self.url)
        # get data from db
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_valid_single_item(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())

        response = self.client.get(
        reverse("todo-detail", kwargs={'pk': todo1.pk}))
        todo = Todo.objects.get(pk=todo1.pk)
        serializer = TodoSerializer(todo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_item(self):
        self.authenticate()
        response = self.client.get(
        reverse("todo-detail", kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_valid_delete_todo(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        response = self.client.delete(
        reverse('todo-detail', kwargs={'pk': todo2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_valid_update_todo(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        updatedata = {"user": 1, "name": "This Item is updated", "timestamp":datetime.now()- timedelta(days = 1)}
        response = self.client.put(
        reverse('todo-detail', kwargs={'pk': todo1.pk}), updatedata)
        todo = Todo.objects.get(pk=todo1.pk)
        serializer = TodoSerializer(todo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class GetAllTodosandEventsTest(APITestCase):
    """ Test module for GET PUT DELETE POST API """

    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        self.user = user

        self.todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        self.todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Event.objects.create(todo= self.todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= self.todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= self.todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= self.todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())

    def authenticate(self):
    
        response = self.client.post(
            reverse("login"),
            {
                "username": "john",
                "password": "johnpassword",
            },
        )
        token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


    def test_get_all(self):
        self.authenticate()
        # get API response
        response = self.client.get(reverse('get_all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_item_with_event(self):
        self.authenticate()
        # get API response
        response = self.client.get(
            reverse('get_event_todo', kwargs={'pk': self.todo1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_duplicate_list_and_item(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        response = self.client.get(
            reverse('duplicate-list', kwargs={'pk': self.todo1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_duplicate_event_test(self):
        self.authenticate()
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        response = self.client.get(
            reverse('duplicate-event', kwargs={'pk': self.todo1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        




