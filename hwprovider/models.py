from django.db import models
from django.utils import dateformat
from django.contrib.auth.models import AbstractBaseUser


class HomeWork(models.Model):
    email = models.EmailField()
    homework_num = models.CharField(max_length=125)
    date = models.DateTimeField(verbose_name="Submitted time", auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Домашка"
        verbose_name_plural = "Домашки"
        ordering = ['-id']

    def __str__(self):
        formatted_date = dateformat.format(self.date, 'Y-m-d [H:i:s]')
        return f"{formatted_date} - {self.email} - {self.homework_num}"


class HomeWorkManager(models.Model):
    aiu_email = models.EmailField(verbose_name="Логин от УИИ", unique=True)
    aiu_password = models.CharField(verbose_name="Пароль от УИИ", max_length=800)

    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ['-id']

    def __str__(self):
        return self.aiu_email

