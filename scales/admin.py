from django.contrib import admin
from django.contrib.auth.models import User
from .models import Person,Assements
class PersonAdmin(admin.ModelAdmin):
    
    list_display=("get_username","get_email","gender","created" )
    def get_username(self, obj):
        return obj.user.username if obj.user else "No user"

    def get_email(self, obj):
        return obj.user.email if obj.user else "No email"

    get_username.short_description = "Username"
    get_email.short_description = "Email"
    
    
     
class AssmeAdmin(admin.ModelAdmin):
    list_display= ("get_username","score_phq9","score_gad7","complete_at")   
    def get_username(self,obj):
        return obj.user.username if obj.user else "No user" 
    get_username.short_description = "Username"

        




admin.site.register(Person,PersonAdmin)
admin.site.register(Assements,AssmeAdmin)

# Register your models here.
