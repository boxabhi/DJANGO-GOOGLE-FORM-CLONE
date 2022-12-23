from django.contrib import admin
from .models import *


admin.site.register(Choices)
admin.site.register(Questions)
admin.site.register(Form)
admin.site.register(Answers)
admin.site.register(Responses)

admin.site.register(User)