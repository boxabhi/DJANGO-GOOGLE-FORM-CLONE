
from django.contrib import admin
from django.urls import path , include
from index.views import LoginView,FormAPI , QuestionAPI , ChoiceAPI , ResponseViewSet,ResponsesAPI,ResgisterView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'response', ResponseViewSet, basename='response')

urlpatterns = [
    path('' , include(router.urls)),
    path('form/', FormAPI.as_view() ),
    path('question/' , QuestionAPI.as_view()),
    path('choices/' , ChoiceAPI.as_view()),
    path('responses/<pk>/' , ResponsesAPI.as_view()),
    path('register/' , ResgisterView.as_view()),
    path('login/' , LoginView.as_view())

]
