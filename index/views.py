from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Form , User , Questions , Choices , Responses , Answers
from .serializers import FormSerializer , QuestionsSerializer , ChoicesSerializer ,ResponsesSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from index.utils.utility import generate_random_string
# GET , POST , PUT , PATCH , DELETE
# 'responses' : [{'question' : 1 , 'answer' : 'Answer'} ,  {'question' : 2 , 'answer' : ['1' ,'2']}]


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Responses.objects.all()
    serializer_class = ResponsesSerializer

    @action(detail=False, methods=['post'])
    def store_responses(self, request):
        try:
            data = request.data

            if data.get('form_id') is None or data.get('responses') is None:
                    return Response(
                        {
                        'status' : False ,
                        'message' : 'form_id and responses both are required',
                        'data' : {}})

            responses = data.get('responses')
            response_obj = Responses.objects.create(
                response_code = generate_random_string(15),
                response_to = Form.objects.get(id = data.get('form_id'))
            )

            for response in responses:
                print(response)
                question_obj = Questions.objects.get(id = response['question'])
                if question_obj.question_type == 'checkbox':
                    for answer in response['answer']:
                        answer_obj = Answers.objects.create(
                                answer = answer,
                                answer_to = question_obj
                        )
                    response_obj.response.add(answer_obj)

                else:
                    answer_obj = Answers.objects.create(
                                answer = response['answer'],
                                answer_to = question_obj
                        )
                    
                    response_obj.response.add(answer_obj)

            return Response({'status' : True ,'message' : 'response captured' , 'data' : {}})

        except Exception as e:
            print(e)
            return Response({'status' : False ,'message' : 'something went wrong' , 'data' : {}})




    


class FormAPI(APIView):

    def get(self , request):
        user = User.objects.get(email="admin@admin.com")
        
        forms = Form.objects.filter(creator = user)

        print(forms)

        if request.GET.get('code'):
            forms = forms.filter(code = request.GET.get('code'))
        
        print(forms.count())

        serializer = FormSerializer(forms , many = True )
        return Response({'status' : True ,'message' : 'forms fetched successfully' , 'data' : serializer.data})


    def post(self , request):
        try:
            data = request.data
            user = User.objects.first()
            form = Form().create_blank_form(user)
            serializer = FormSerializer(form)
            return Response({
                'status': True,
                'message' : 'form created successfully',
                'data' : serializer.data
            })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })
            
        

    def patch(self , request):
        try:
            data = request.data
            if not data.get('form_id'):
                return Response({
                'status': False,
                'message' : 'form_id is required',
                'data' : {}
            })
            

            form_obj = Form.objects.filter(code = data.get('form_id'))

            if form_obj.exists():
                serializer = FormSerializer(form_obj[0] , data= data , partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                    'status': True,
                    'message' : 'form updated successfully',
                    'data' : serializer.data
                    })
                return Response({
                    'status': False,
                    'message' : 'form not updated',
                    'data' : serializer.errors
                })

            return Response({
                    'status': False,
                    'message' : 'invalid form_id',
                    'data' : {}
                })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })
        

class QuestionAPI(APIView):

    def post(self , request):
        try:

            data = request.data
            data['question'] = 'Untitled Question'
            data['question_type'] = 'multiple choice'
            
            if not data.get('form_id'):
                    return Response({
                    'status': False,
                    'message' : 'form_id is required',
                    'data' : {}
                })
        
            serializer = QuestionsSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                choice = Choices.objects.create(choice = 'Option')
                quesiton_obj = Questions.objects.get(id = serializer.data['id'])
                quesiton_obj.choices.add(choice)
                form = Form.objects.get(id = data['form_id'])
                form.questions.add(quesiton_obj)

                form_serializer = FormSerializer(form)

                return Response({
                    'status' : True,
                    'data' : form_serializer.data,
                    'message' : 'question created'
                })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })

    
    def patch(self , request):
        try:
            data = request.data
            if not data.get('question_id'):
                return Response({
                'status': False,
                'message' : 'question_id is required',
                'data' : {}
            })

            question_obj = Questions.objects.filter(id = data.get('question_id'))

            if not question_obj.exists():
                return Response({
                'status': False,
                'message' : 'invalid question_id',
                'data' : {}
                })

            serializer = QuestionsSerializer(question_obj[0] , data = data , partial = True)
           
            if serializer.is_valid():
                serializer.save()
                form = Form.objects.get(id = data['form_id'])
                
                form_serializer = FormSerializer(form)
                return Response({
                    'status' : True,
                    'data' : form_serializer.data,
                    'message' : 'question updated'
                })

            return Response({
                'status': False,
                'message' : 'form not updated',
                'data' : serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })

    def delete(self , request):
        try:
            data = request.data
            
            if not data.get('question_id') or not data.get('form_id'):
                return Response({
                'status': False,
                'message' : 'question_id & form_id are required',
                'data' : {}
            })

            try:
                question_obj = Questions.objects.get(id = data.get('question_id'))
                question_obj.delete()
                form = Form.objects.get(id = data['form_id'])
                form_serializer = FormSerializer(form)
                return Response({
                    'status' : True,
                    'data' : form_serializer.data,
                    'message' : 'question created'
                })



            except Exception as e:
                print(e)
                return Response({
                'status': False,
                'message' : 'invalid question_id ',
                'data' : {}
            })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })
            

class ChoiceAPI(APIView):
    def post(self , request):
        data = request.data
        if not data.get('form_id') or not data.get('question_id'):
            return Response({
                'status': False,
                'message' : 'form_id and question_id is required',
                'data' : {}
            })

        data['choice'] = 'Option'
        serializer  = ChoicesSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            form = Form.objects.get(id = data['form_id'])
            form.questions.get(id = data['question_id']).choices.add(Choices.objects.get(id = serializer.data['id']))
           
            form_serializer = FormSerializer(form)
            return Response({
                'status' : True,
                'data' : form_serializer.data,
                'message' : 'choices created'
            })

          
        return Response({
                'status': False,
                'message' : 'form not updated',
                'data' : serializer.errors
                })
    
    def patch(self , request):
        try:
            data = request.data
            if not data.get('choice_id') or not data.get('form_id'):
                return Response({
                    'status' : False,
                    'message' : 'choice_id is required',
                    'data' : {}
                })

            choice_obj = Choices.objects.filter(id = data.get('choice_id'))

            if not choice_obj.exists():
                return Response({
                'status': False,
                'message' : 'invalid choice_id',
                'data' : {}
                })

            serializer = ChoicesSerializer(choice_obj[0] , data = data , partial = True)
            if serializer.is_valid():
                serializer.save()
                form = Form.objects.get(id = data['form_id'])
                form_serializer = FormSerializer(form)
                return Response({
                    'status' : True,
                    'data' : form_serializer.data,
                    'message' : 'choice updated'
                })

            return Response({
                'status': False,
                'message' : 'form not updated',
                'data' : serializer.errors
                })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })

    def delete(self , request):
        try:
            data = request.data
            
            if not data.get('choice_id') or not data.get('form_id'):
                return Response({
                'status': False,
                'message' : 'choice_id & form_id are required',
                'data' : {}
            })

            try:
                choice_obj = Choices.objects.get(id = data.get('choice_id'))
                choice_obj.delete()
                form = Form.objects.get(id = data['form_id'])
                form_serializer = FormSerializer(form)
                return Response({
                    'status' : True,
                    'data' : form_serializer.data,
                    'message' : 'question created'
                })



            except Exception as e:
                print(e)
                return Response({
                'status': False,
                'message' : 'invalid choice_id ',
                'data' : {}
            })

        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message' : 'something went wrong',
                'data' : {}
            })



from django.db.models import Count

class ResponsesAPI(APIView):
    def get(self , request):
        try:
            formInfo = Form.objects.first()
            responses = Responses.objects.filter(response_to = formInfo)
        
           
            responsesSummary = []
            choiceAnswered = {}
            non_choices_answer = {}


            for question in formInfo.questions.all():
                answers = Answers.objects.filter(answer_to = question.id)
                if question.question_type == "multiple choice" or question.question_type == "checkbox":
                    choiceAnswered[question.question] = choiceAnswered.get(question.question, {})

                    for choice in question.choices.all():
                        choiceAnswered[question.question][choice.choice] = 0


                    for answer in answers:
                        print(answer)
                        choice = answer.answer_to.choices.get(choice = answer.answer).choice
                        
                        choiceAnswered[question.question][choice] = choiceAnswered.get(question.question, {}).get(choice, 0) + 1
                
                else:
                    for answer in answers:
                        if non_choices_answer.get(question.question):
                            non_choices_answer[question.question].append(answer.answer)
                        else:
                            non_choices_answer[question.question] = [answer.answer]




                responsesSummary.append({"question": question, "answers":answers })


          
            final_list = []
            for answr in choiceAnswered:
                final_dict = {}
                final_dict['question']  = answr
                final_dict['answer'] = choiceAnswered[answr]

                final_dict['chartData'] = {
                    'labels' : choiceAnswered[answr].keys(),
                    'datasets' : [{'data' : choiceAnswered[answr].values()}]
                }

                final_dict['keys'] = choiceAnswered[answr].keys()
                final_dict['values'] = choiceAnswered[answr].values()

                final_list.append(final_dict)
                

            return Response({
                'message' : True,
                'data' : final_list,
                'non_choices_answer' : non_choices_answer
            })
        
        except Exception as e:
            import sys, os
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            return Response({
                'message' : 'wrong'
            })