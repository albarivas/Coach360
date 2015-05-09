'''
@author: lowcoupling
'''
from spices.coach360.models import Survey,Question,Response
from django.contrib import admin


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3
    
class Coach360Admin(admin.ModelAdmin):
    inlines = [QuestionInline]
    
#admin.site.register(Question,Coach360Admin)
admin.site.register(Survey,Coach360Admin)

