from rest_framework import serializers
from .models import Todo, Event

class TodoSerializer(serializers.ModelSerializer):
    """ 
    TodoSerializer converts Todo querysets and model instances into native 
    Python datatypes so that it rendered into JSON , XML or other content types.
    """
    class Meta:
        model = Todo
        fields = '__all__'
        
       
class EventSerializer(serializers.ModelSerializer):
    """ 
    EventSerializer converts Event querysets and model instances into native 
    Python datatypes so that it rendered into JSON , XML or other content types.
    """

    class Meta:
        model = Event
        fields = '__all__'
 

