from django.db import models
from django.contrib.auth.models import User

class Applicants(models.Model):
    first_name = models.CharField(max_length=100, help_text='Имя заявителя', verbose_name='Имя',null=True,blank=True)
    last_name = models.CharField(max_length=100, help_text='Фамилия заявителя', verbose_name='Фамилия',null=True,blank=True)
    patronymic = models.CharField(max_length=100, help_text='Отчество заявителя', verbose_name='Отчество', blank=True, null=True)
    phone = models.CharField(max_length=20, help_text='Номер телефона',verbose_name='Номер телефона',null=True,blank=True)
    email = models.EmailField(help_text='Почта',verbose_name='Почта',null=True,blank=True)
    org = models.CharField(max_length=200,help_text='Организация',verbose_name='Организация',null=True,blank=True)
    id_user_tel = models.CharField(null=True, blank=True, verbose_name='ИД телеграмм пользователя', max_length=100)
    black_list = models.BooleanField(default=False,help_text='ЧС', verbose_name='ЧС')
    class Meta:
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'
        ordering = ['last_name']
    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'

class Organizations(models.Model):
    name = models.CharField(max_length=300,null=True,blank=True,help_text='Название организации',verbose_name='Имя')
    inn = models.CharField(max_length=10,null=True)
    status = models.BooleanField(default=False,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    date_completion = models.DateTimeField(auto_now=True,null=True)
    id_appl = models.ForeignKey(Applicants,on_delete=models.CASCADE,verbose_name='Заявитель')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['date_created']

    def __str__(self):
        return f'{self.name} инн - {self.inn}'


class Person(models.Model):
    first_name = models.CharField(max_length=100,help_text = 'Имя персоны',verbose_name='Имя')
    last_name = models.CharField(max_length=100, help_text='Фамилия персоны',verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, help_text='Отчество персоны',verbose_name='Отчество',blank=True,null=True)
    status = models.BooleanField(default=False,verbose_name='Статус заявки')
    date_created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    date_completion = models.DateTimeField(auto_now=True,null=True)
    id_appl = models.ForeignKey(Applicants,on_delete=models.CASCADE,verbose_name='Заявитель')
    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'
        ordering = ['date_created']


    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'



class Contact(models.Model):
    first_name = models.CharField(max_length=100, help_text='Имя персоны',verbose_name='Имя')
    last_name = models.CharField(max_length=100, help_text='Фамилия персоны',verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, help_text='Отчество персоны',verbose_name='Отчество', blank=True, null=True)
    status = models.BooleanField(default=False,verbose_name='Статус заявки')
    date_created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания заявки')
    date_completion = models.DateTimeField(auto_now=True,null=True)
    inn = models.CharField(max_length=10,verbose_name='ИНН организации')
    post = models.CharField(max_length=100,help_text='Должность',verbose_name='Должность')
    id_appl = models.ForeignKey(Applicants,on_delete=models.CASCADE,verbose_name='Заявитель')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['date_created']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

class Systems(models.Model):
    name = models.CharField(max_length=300,help_text='Название системы',verbose_name='Название системы')
    description = models.TextField(help_text='Описание системы',verbose_name='Описание системы',blank=True,null=True)
    class Meta:
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'
    def __str__(self):
        return self.name


class Other_applications(models.Model):
    system = models.ForeignKey(Systems,on_delete=models.CASCADE,verbose_name='Система')
    text = models.TextField(verbose_name = 'Текст заявки',null=True)
    date_created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания заявки')
    date_completion = models.DateTimeField(auto_now=True,null=True)
    status = models.BooleanField(default=False, verbose_name='Статус заявки')
    id_appl = models.ForeignKey(Applicants, on_delete=models.CASCADE, verbose_name='Заявитель')
    answer = models.TextField(verbose_name = 'Текст ответа',null=True,blank=True)
    responsible = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['date_created']
    def __str__(self):
        return f'{self.system} - {self.id_appl}'

class Typical_answers(models.Model):
    name = models.CharField(max_length=300,verbose_name='Наименование')
    text = models.TextField(verbose_name = 'Текст ответа',null=True)
    system = models.ForeignKey(Systems,on_delete=models.CASCADE,verbose_name='Система')

    class Meta:
        verbose_name = 'Шаблонный ответ'
        verbose_name_plural = 'Шаблонные ответы'
        ordering = ['-id']

    def __str__(self):
        return self.name




