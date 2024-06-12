from django.contrib import admin

from .models import *
admin.site.register(Quiz_category)
admin.site.register(Quiz)

class AnswerInLine(admin.TabularInline):
    model = Answer
    
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)


class Marks_Of_UserAdmin(admin.ModelAdmin):
    readonly_fields=('score', 'user_responses')

admin.site.register(Marks_Of_User,Marks_Of_UserAdmin)



