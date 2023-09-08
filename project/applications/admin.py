from django.contrib import admin
from .models import Organizations,Person,Contact,Systems,Other_applications,Applicants,Typical_answers


@admin.register(Applicants)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'patronymic',  'phone',]
    list_filter = ['org']
    search_fields = ['last_name']

@admin.register(Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ['name','inn','status','date_completion']
    list_filter = ['status']
    search_fields = ['id']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','patronymic','status']
    list_filter = ['status']
    search_fields = ['id','last_name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','patronymic','inn','status']
    list_filter = ['status']
    search_fields = ['id']

@admin.register(Systems)
class SystemsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Other_applications)
class OtherApplicationsAdmin(admin.ModelAdmin):
    list_display = ['system', 'id_appl', 'date_created',  'status']
    list_filter = ['status']
    search_fields = ['id_appl']

@admin.register(Typical_answers)
class TypicalAnswersAdmin(admin.ModelAdmin):
    list_display = ['name','system']