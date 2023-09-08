import datetime
import os

from django.shortcuts import render,redirect, get_object_or_404
from .models import Contact,Organizations,Person,Other_applications,Systems,Typical_answers
from django.contrib.auth.models import User

from .forms import AnswerForm

from dotenv import load_dotenv
import telebot

from django.core.paginator import Paginator

from django.utils import timezone
import zoneinfo

def search_appl(request,f_name=None,s_name=None,patr = None):
    f_name = request.GET.getlist('f_name')
    s_name = request.GET.getlist('s_name')
    patr = request.GET.getlist('patr')
    print(f_name,s_name,patr)
    if len(f_name) == 0 and len(s_name)==0 and len(patr)==0:
        f_name.append('')
        s_name.append('')
        patr.append('')
    applications = Other_applications.objects.filter(
        id_appl__first_name=f_name[0],
        id_appl__last_name=s_name[0],
        id_appl__patronymic=patr[0],
    )
    context = {
        'applications':applications
    }
    return render(request,'applications/search_appl.html',context = context)




def index(request,days = 'все время'):
    load_dotenv()
    page = os.getenv('PAGINATOR')
    systems = Systems.objects.all()
    get_system = request.GET.getlist('system')
    get_start = request.GET.getlist('start')
    get_stop = request.GET.getlist('stop')

    if len(get_start) == 0 and len(get_stop) == 0:
        get_start.append('')
        get_stop.append('')
    if len(get_system) == 0:
        if len(get_start[0]) != 0 and len(get_stop[0]) != 0:
            applications = Other_applications.objects.filter(
                                                             date_created__gte=get_start[0],
                                                             date_created__lte=get_stop[0],
            )

            days = (datetime.datetime.strptime(get_stop[0], '%Y-%m-%d') - datetime.datetime.strptime(get_start[0], '%Y-%m-%d')).days + 1
            if days == 1:
                days = str(days) + ' сутки'
            else:
                days = str(days) + ' суток'

        else:
            applications = Other_applications.objects.all()

    else:
        if len(get_start[0]) != 0 and len(get_stop[0]) != 0:
            days = (datetime.datetime.strptime(get_stop[0], '%Y-%m-%d') - datetime.datetime.strptime(get_start[0],
                                                                                                     '%Y-%m-%d')).days + 1
            if days == 1:
                days = str(days) + ' сутки'
            else:
                days = str(days) + ' суток'

            applications = Other_applications.objects.filter(
                                                             date_created__gte=get_start[0],
                                                             date_created__lte=get_stop[0],
                                                             system_id__in=request.GET.getlist('system'))
        else:
            applications = Other_applications.objects.filter(system_id__in=request.GET.getlist('system'))
    count = applications.count()
    paginator = Paginator(applications, page)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)
    context = {
        'applications': applications,
        'count':count,
        'days':days,
        'systems':systems
    }
    return render(request,'applications/index.html',context=context)


def get_contact(request,id_appl=None):
    if id_appl==None:
        contacts = Contact.objects.filter(status=False)
    else:
        contacts = Contact.objects.filter(status=False,id_appl=id_appl)
    load_dotenv()
    page = os.getenv('PAGINATOR')
    contacts = Paginator(contacts, page)
    page_number = request.GET.get('page')
    contacts = contacts.get_page(page_number)
    context = {'contacts':contacts}
    return render(request,'applications/contacts.html',context=context)


def get_organization(request,id_appl=None):
    if id_appl == None:
        organizations = Organizations.objects.filter(status=False)
    else:
        organizations = Organizations.objects.filter(status=False,id_appl=id_appl)
    load_dotenv()
    page = os.getenv('PAGINATOR')
    organizations = Paginator(organizations, page)
    page_number = request.GET.get('page')
    organizations = organizations.get_page(page_number)
    context = {'organizations': organizations}
    return render(request, 'applications/organizations.html', context=context)

def get_person(request):
    persons = Person.objects.filter(status=False)
    load_dotenv()
    page = os.getenv('PAGINATOR')
    persons = Paginator(persons, page)
    page_number = request.GET.get('page')
    persons = persons.get_page(page_number)
    context = {'persons': persons}
    return render(request, 'applications/persons.html', context=context)


def close_applications(request):
    systems = Systems.objects.all()
    get_system = request.GET.getlist('system')
    get_start = request.GET.getlist('start')
    get_stop = request.GET.getlist('stop')

    if len(get_start)==0 and len(get_stop)==0:
        get_start.append('')
        get_stop.append('')
    if request.user.is_authenticated is False:
        return redirect('admin:index')

    if len(get_system) == 0:
        if len(get_start[0]) != 0 and len(get_stop[0]) != 0:
            applications = Other_applications.objects.filter(status=True,
                                                             date_created__gte=get_start[0],
                                                             date_created__lte=get_stop[0])
        else:
            applications = Other_applications.objects.filter(status=True)
    else:
        if len(get_start[0]) != 0 and len(get_stop[0]) != 0:

            applications = Other_applications.objects.filter(status=True,
                                                             date_created__gte=get_start[0],
                                                             date_created__lte=get_stop[0],
                                                             system_id__in=request.GET.getlist('system'))
        else:
            applications = Other_applications.objects.filter(status=True, system_id__in=request.GET.getlist('system'))
    load_dotenv()
    page = os.getenv('PAGINATOR')
    applications = Paginator(applications, page)
    page_number = request.GET.get('page')
    applications = applications.get_page(page_number)
    context = {
        'applications': applications,
        'systems': systems,
    }

    return render(request, 'applications/close_applications.html', context=context)

def get_applications(request):
    load_dotenv()
    page = os.getenv('PAGINATOR')

    systems = Systems.objects.all()
    get_system = request.GET.getlist('system')
    get_start = request.GET.getlist('start')
    get_stop = request.GET.getlist('stop')
    if len(get_start)==0 and len(get_stop)==0 and len(get_system)==0:
        get_stop.append('')
        get_start.append('')
    if request.user.is_authenticated is False:
        return redirect('admin:index')
    if request.user.is_superuser:
        if len(get_system)==0:
            if len(get_start[0])!= 0 and len(get_stop[0])!= 0:

                applications = Other_applications.objects.filter(status=False,
                                                                 date_created__gte=get_start[0],
                                                                 date_created__lte=get_stop[0])
            else:
                applications = Other_applications.objects.filter(status=False)
        else:
            if len(get_start[0]) != 0 and len(get_stop[0]) != 0:

                applications = Other_applications.objects.filter(status=False,
                                                                 date_created__gte=get_start[0],
                                                                 date_created__lte=get_stop[0],
                                                                 system_id__in=request.GET.getlist('system'))
            else:
                applications = Other_applications.objects.filter(status=False,system_id__in=request.GET.getlist('system'))
        responsibles = User.objects.all()

        applications = Paginator(applications, page)
        page_number = request.GET.get('page')
        applications = applications.get_page(page_number)
        context = {
                'applications': applications,
                'systems': systems,
                'responsibles': responsibles
            }

        return render(request, 'applications/applications_admin.html', context=context)
    else:
        if len(get_system)==0:
            if len(get_start[0])!=0 and  len(get_stop[0])!=0:

                applications = Other_applications.objects.filter(status=False, responsible__username=request.user,date_created__gte=get_start[0],date_created__lte=get_stop[0])
            else:
                applications = Other_applications.objects.filter(status=False,responsible__username=request.user)
        else:
            if len(get_start[0]) != 0 and len(get_stop[0]) != 0:
                applications = Other_applications.objects.filter(system_id__in=request.GET.getlist('system'), status=False,
                                                             responsible__username=request.user,date_created__gte=get_start[0],date_created__lte=get_stop[0])
            else:
                applications = Other_applications.objects.filter(system_id__in=request.GET.getlist('system'),
                                                                 status=False,
                                                                 responsible__username=request.user)
    applications = Paginator(applications, page)
    page_number = request.GET.get('page')
    applications = applications.get_page(page_number)
    context = {
        'applications': applications,
        'systems': systems
    }
    return render(request, 'applications/applications.html', context=context)

def give_responsible(request,id_res,id_appl):
    appl = Other_applications.objects.get(id = id_appl)
    appl.responsible =  User.objects.get(id=id_res)
    appl.save()
    return redirect('applications:applications')


def off_person(request,id_person):
    person = Person.objects.get(pk=id_person)
    person.status = True
    person.save()
    bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ", parse_mode=None)
    bot.send_message(person.id_appl.id_user_tel, f'Ваша заявка (добавление контрагента {person.first_name} {person.last_name} {person.patronymic}) успешно выполнена')
    return redirect('applications:persons')

def off_org(request,id_org):
    org = Organizations.objects.get(pk=id_org)
    org.status = True
    org.save()
    bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ",parse_mode=None)
    bot.send_message(org.id_appl.id_user_tel,f'Ваша заявка (добавление контрагента {org.name} инн {org.inn}) успешно выполнена')
    return redirect('applications:organizations')

def repl_org(request,id_org):
    org = Organizations.objects.get(pk=id_org)
    org.status = True
    org.save()
    bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ",parse_mode=None)
    bot.send_message(org.id_appl.id_user_tel,f'Контрагент {org.name} инн {org.inn}) уже присутствовал в справочнике организаций в ЕСЭД! Обязательно проверяйте при направлении заявки')
    return redirect('applications:organizations')

def off_contact(request,id_cont):
    contact= Contact.objects.get(pk=id_cont)
    contact.status = True
    contact.save()
    bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ",parse_mode=None)
    bot.send_message(contact.id_appl.id_user_tel,f'Ваша заявка (добавление контрагента {contact.first_name} {contact.last_name} {contact.patronymic} - {contact.post} успешно выполнена')
    return redirect('applications:contacts')

def off_appl(request,id_appl):
    appl= Other_applications.objects.get(pk=id_appl)
    appl.status = True
    appl.save()
    bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ",parse_mode=None)
    bot.send_message(appl.id_appl.id_user_tel,f'Ваша заявка {appl.text[:15]}... успешно выполнена')
    return redirect('applications:applications')

load_dotenv()
ans = os.getenv('ANSWER')


def appl(request,id_appl):
    global ans
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_r = form.cleaned_data['answer']
            appl = Other_applications.objects.get(pk=id_appl)
            appl.status = True
            appl.answer = answer_r
            appl.save()
            bot = telebot.TeleBot("5665489116:AAHgcRN2ByOHqsSMXPr8Yi1o5fHmngwqSqQ", parse_mode=None)
            bot.send_message(appl.id_appl.id_user_tel, f'Ваша заявка № {appl.id} успешно выполнена \n {answer_r} \n {ans}')
            return redirect('applications:applications')
    #my_instance = get_object_or_404(Other_applications, pk=id_appl)
    article = Other_applications.objects.get(pk=id_appl)
    form = AnswerForm(instance=article)
    appl = Other_applications.objects.get(pk=id_appl)
    templ = Typical_answers.objects.filter(system=appl.system)
    content = {
        'application':appl,
        'form':form,
        'templates':templ,
    }
    return render(request,'applications/application.html',context = content)

def templ_appl(request,id_appl,id_templ_answer):
    appl = Other_applications.objects.get(pk=id_appl)
    text = Typical_answers.objects.get(id = id_templ_answer).text
    appl.answer = text
    appl.save()
    article = Other_applications.objects.get(pk=id_appl)
    form = AnswerForm(instance=article)
    appl = Other_applications.objects.get(pk=id_appl)
    templ = Typical_answers.objects.filter(system=appl.system)
    content = {
        'application': appl,
        'form': form,
        'templates': templ,
    }
    return redirect('applications:appl',id_appl=id_appl)

