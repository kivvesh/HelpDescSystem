from django.contrib import admin
from django.urls import path
from .views import get_contact,get_organization,get_person,off_person,off_org,off_contact,get_applications,\
    off_appl,appl,give_responsible,close_applications,index,search_appl,repl_org,templ_appl

app_name = 'applications'

urlpatterns = [
    path('contacts/',get_contact, name = 'contacts'),
    path('organizations/',get_organization,name = 'organizations'),
    path('persons/',get_person,name = 'persons'),
    path('applications/',get_applications,name = 'applications'),
    path('person/<int:id_person>/',off_person,name = 'off_person'),
    path('organizations/<int:id_org>/',off_org,name = 'off_org'),
    path('organizations_repl/<int:id_org>/',repl_org,name = 'repl_org'),
    path('contacts/<int:id_cont>/',off_contact,name = 'off_contact'),
    path('applications/<int:id_appl>/',off_appl,name = 'off_appl'),
    path('application/<int:id_appl>/',appl,name = 'appl'),
    path('application/<int:id_appl>/<int:id_templ_answer>/',templ_appl,name = 'templ_appl'),
    path('give_responsible/<int:id_res>-<int:id_appl>/',give_responsible,name = 'give_resp'),
    path('close_apple/',close_applications,name = 'close_applications'),
    path('search_appl/',search_appl,name = 'search_appl'),
    path('',index,name = 'index'),
]