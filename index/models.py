from django.db import models
from django.contrib.auth.models import User , AbstractUser
from .choices import QUESTION_CHOICES
from .utils.utility import generate_random_string

# DRY => Do not repeat yourself

class User(AbstractUser, models.Model):
    USERNAME_FIELD = "email"
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []



class BaseModel(models.Model):
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True



class Choices(BaseModel):
    choice = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.choice

    class Meta:
        db_table = "choices"
        ordering = ['-choice']

       

class Questions(BaseModel):
    question = models.CharField(max_length=100)
    question_type = models.CharField(choices = QUESTION_CHOICES , max_length=100)
    required = models.BooleanField(default=False)
    choices = models.ManyToManyField(Choices , related_name="question_choices" , blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self) -> str:
        return self.question


class Form(BaseModel):
    code = models.CharField(max_length=100 , unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creator = models.ForeignKey(User , on_delete=models.CASCADE)
    background_color = models.CharField(max_length=100 , default="#272124")
    collect_email = models.BooleanField(default=False)
    questions = models.ManyToManyField(Questions , related_name="questions")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @staticmethod
    def create_blank_form(user):
        form_token = generate_random_string()
        choices = Choices.objects.create(choice ="Option 1")
        question = Questions.objects.create(question_type = 'multiple choice' , question="Untitled question" , )
        question.choices.add(choices)

        forms = Form.objects.filter(creator = user).last()

        form = Form(code = form_token , title = f"Untiled Form {forms.pk + 1}"  , description="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,", creator = user)
        form.save()
        form.questions.add(question)
        return form

    def __str__(self) -> str:
        return self.title


class Answers(BaseModel):
    answer = models.CharField(max_length=100)
    answer_to = models.ForeignKey(Questions , on_delete=models.CASCADE , related_name="answer_to")


    def __str__(self) -> str:
        return self.answer


class Responses(BaseModel):
    response_code= models.CharField(max_length=100 , unique=True)
    response_to = models.ForeignKey(Form , on_delete=models.CASCADE)
    responder_ip = models.CharField(max_length=100)
    responder_email = models.EmailField(null=True , blank=True)
    response = models.ManyToManyField(Answers , related_name="answers")
