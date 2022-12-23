from rest_framework import serializers
from .models import (
    Form,
    Choices,
    Questions,
    Answers,
    Responses
)


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ['created_at' , 'updated_at']
    
    def to_representation(self, instance):
        questions = instance.questions.all()
        question_serializer = QuestionsSerializer(questions , many = True)
        payload = {
            'form' : instance.id,
            'code' : instance.code,
            'title' : instance.title,
            'description' : instance.description,
            'creator' : instance.creator.username,
            'background_color' : instance.background_color,
            'questions' : question_serializer.data
        }
        return payload

    

class ChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choices
        exclude = ['created_at' , 'updated_at']


class QuestionsSerializer(serializers.ModelSerializer):
    choices = ChoicesSerializer(read_only = True ,many =True)

    class Meta:
        model = Questions
        exclude = ['created_at' , 'updated_at']
    




class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        exclude = ['created_at' , 'updated_at']


class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        exclude = ['created_at' , 'updated_at']





