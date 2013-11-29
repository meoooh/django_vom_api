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
    list_display = ('writer', '__unicode__', 'creation', 'modification')

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation', 'modification')

admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Constellation)
admin.site.register(History, HistoryAdmin)
admin.site.register(Item)

