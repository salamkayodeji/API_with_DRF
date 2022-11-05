from django.urls import path, include
from todo import views 
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




router = routers.DefaultRouter()
router.register(r'todo', views.TodoViewSet, 'todo'),
router.register(r'event', views.EventViewSet, 'event'),


urlpatterns = [
    path('', include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
	path('duplicate_list/<int:pk>', views.Duplicate_List, name="duplicate-list"),
	path('duplicate_event/<int:pk>', views.Duplicate_Event, name="duplicate-event"),
    path('get_all/', views.Get_Todo_Event, name='get_all' ),
    path('get_event/<int:pk>', views.get_events, name='get_event' ),
    path('get_event_todo/<int:pk>', views.get_events_todo, name='get_event_todo' ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('openapi/', get_schema_view(
        title="Todo Micro-Service",
        description="API developers hoping to use our service"
    ), name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='todo/documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

]
