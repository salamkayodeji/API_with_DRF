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
    """ Test all API ENDPOINTS for Events API """

    def setUp(self):
        self.url = reverse("event-list")
        """ Used to create user that will be used to test all EVENT api end points """        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        self.user = user

        
    def authenticate(self):
        """ Used to authenticate User, it returns a authenticated User """
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
        """
        Ensure we can create a new Events object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        #Create a sample event data with todo
        sample_data = {"todo": 1, "event_name": "Sample Items to do now", "complete":True,  "date_created":date.today(), "last_modified":date.today()}
        response = self.client.post(reverse("event-list"), sample_data)
        #check if it returns the right status code and sample data is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_events(self):
        """
        Ensure we can get all event objects.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        #Create events data with todo
        Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        # get API response.
        response = self.client.get(self.url)
        # get data from db.
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_valid_single_event(self):
        """
        Ensure we can get a single event object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        #Create events data with todo
        event1 = Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        # get API response.
        response = self.client.get(
        reverse("event-detail", kwargs={'pk': event1.pk}))
        # get data from db.
        event = Event.objects.get(pk=event1.pk)
        serializer = EventSerializer(event)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_event(self):
        """
        Ensure it returns nothing when we try to get an item that does not exist.
        """
        self.authenticate()
        response = self.client.get(
        reverse("event-detail", kwargs={'pk': 30}))
        #check if it returns the right status code for item not found.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_valid_delete_event(self):
        """
        Ensure we can delete a single event object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        #Create events data with todo
        event1 = Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        # get API response.
        response = self.client.delete(
        reverse('todo-detail', kwargs={'pk': event2.pk}))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_valid_update_event(self):
        """
        Ensure we can update an event object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        self.todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        self.todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        #Create events data with todo
        event1 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        event2 = Event.objects.create(todo= self.todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        event3 = Event.objects.create(todo= self.todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        event4 = Event.objects.create(todo= self.todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        #Create a sample event data with todo to update with
        updatedata = {"todo": 2, "event_name": "This Item is updated", "complete":True, "date_created":date.today() - timedelta(days = 1), "last_modified":date.today()}
        # get API response.
        response = self.client.put(
        reverse('event-detail', kwargs={'pk': event1.pk}), updatedata)
        # get data from db.
        event = Event.objects.get(pk=event1.pk)
        serializer = EventSerializer(event)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TodoListCreateTestCase(APITestCase):
    """ Test all API ENDPOINTS for Todo API """
    def setUp(self):
        self.url = reverse("todo-list")
        """ Used to create user that will be used to test all Todo api end points """        
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        self.user = user

        
    def authenticate(self):
        """ Used to authenticate User, it returns a authenticated User """
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
        """
        Ensure we can create a new Events object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        #Create a sample Todo data.
        sample_data = {"user": 1, "name": "Sample Items to do", "timestamp":datetime.now()}
        response = self.client.post(reverse("todo-list"), sample_data)
        #check if it returns the right status code and sample data is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_todos(self):
        """
        Ensure we can get all Todo objects.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        #Create Todo objects.
        Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        # get API response
        response = self.client.get(self.url)
        # get data from db
        todo = Todo.objects.all()
        serializer = TodoSerializer(todo, many=True)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_valid_single_todo(self):
        """
        Ensure we can get a single Todo object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        #Create Todo objects 
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        # get API response.
        response = self.client.get(
        reverse("todo-detail", kwargs={'pk': todo1.pk}))
        # get data from db.
        todo = Todo.objects.get(pk=todo1.pk)
        serializer = TodoSerializer(todo)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invalid_single_item(self):
        """
        Ensure it returns nothing when we try to get an item that does not exist.
        """
        self.authenticate()
        response = self.client.get(
        reverse("todo-detail", kwargs={'pk': 30}))
        #check if it returns the right status code for item not found.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_valid_delete_todo(self):
        """
        Ensure we can delete a single Todo object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        #Create Todo objects.
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        # get API response.
        response = self.client.delete(
        reverse('todo-detail', kwargs={'pk': todo2.pk}))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_valid_update_todo(self):
        """
        Ensure we can update an event object.
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        #Create Todo objects.
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        todo3 = Todo.objects.create(user= self.user, name= "Sample Items I did yesterday", timestamp=datetime.now()- timedelta(days = 1))
        todo4 = Todo.objects.create(user= self.user, name= "Sample Items to do", timestamp=datetime.now())
        #Create a sample Todo data to update with
        updatedata = {"user": 1, "name": "This Item is updated", "timestamp":datetime.now()- timedelta(days = 1)}
        # get API response.
        response = self.client.put(
        reverse('todo-detail', kwargs={'pk': todo1.pk}), updatedata)
        # get data from db.
        todo = Todo.objects.get(pk=todo1.pk)
        serializer = TodoSerializer(todo)
        #check if api reponse is the same with data gotten from db.
        self.assertEqual(response.data, serializer.data)
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)




class GetAllTodosandEventsTest(APITestCase):
    """
        Ensure we can:
        1)  get all Todos and the Events
        2)  get all Events and the Todo it related to
        3)  duplicate the Todo and all Events related to it
        4)  duplicate a singular Event related to a Todo
    """

    def setUp(self):
        """ Used to create user that will be used to test end point """        
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
        """
        get all Todos and the Events.
        
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # get API response
        response = self.client.get(reverse('get_all'))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_item_with_event(self):
        """
        get all Events and the Todo it related to.
        
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # get API response
        response = self.client.get(
            reverse('get_event_todo', kwargs={'pk': self.todo1.pk}))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_duplicate_list_and_item(self):
        """     
        duplicate the Todo and all Events related to it        
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # get API response.
        response = self.client.get(
            reverse('duplicate-todo', kwargs={'pk': self.todo1.pk}))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_duplicate_event_test(self):
        """     
        duplicate a singular Event related to a Todo
        """
        #Make all requests in the context of a logged in session.
        self.authenticate()
        # Create a new Todo inorder to get todoid to create events
        todo1 = Todo.objects.create(user= self.user, name= "Sample Items to do now", timestamp=datetime.now())
        todo2 = Todo.objects.create(user= self.user, name= "Sample Items to do for today", timestamp=datetime.now())
        #Create events data with todo
        Event.objects.create(todo= todo1, event_name= "Sample Items to do now", complete=True,  date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo1, event_name= "Sample Items to do for today", complete=False, date_created=date.today(), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items I did yesterday", complete=True, date_created=date.today()- timedelta(days = 1), last_modified=date.today())
        Event.objects.create(todo= todo2, event_name= "Sample Items to do", complete=True, date_created=date.today(), last_modified=date.today())
        # get API response.
        response = self.client.get(
            reverse('duplicate-event', kwargs={'pk': self.todo1.pk}))
        #check if it returns the right status code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        




