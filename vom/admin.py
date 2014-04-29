from django.contrib import admin
from vom.models import *
from django.contrib.auth import get_user_model

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'birthday', 'creation', 'modification')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation', 'modification')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', '__unicode__', 'creation', 'modification')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'writer', 'creation', 'modification')

admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Item)
admin.site.register(TypeOfItem)
admin.site.register(ItemBox)
admin.site.register(ActivityLog)
