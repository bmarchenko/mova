#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from django.db import models
from autoslug import AutoSlugField



class Region(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

class Place(models.Model):
    TYPE_CHOICES = (
        ("lang-shop", u"Магазин"),
        ("lang-cafe", u"Заклад Харчування"),
        ("lang-pharmacy", u"Aптека"),
        ("lang-gasstation", u"ФЗС")
    )
    COLOR_CHOICES = (
        (1, u"червоний"),
        (2, u"жовтий"),
        (3, u"зелений")
    )
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    owner = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="title")
    color = models.IntegerField(choices=COLOR_CHOICES)
    type = models.CharField(choices=TYPE_CHOICES, max_length=100)
    region = models.ForeignKey(Region)
    created_at = models.DateField(default=datetime.date.today)

    def __unicode__(self):
        return self.title

class Profile(models.Model):
    GENDER_CHOICES = (
        (1, u"Чоловіча"),
        (2, u"Жіноча")
    )
    gender = models.IntegerField(choices=GENDER_CHOICES)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    email = models.EmailField()
    phone = models.IntegerField()

class Poll(models.Model):
    NO_UKR_CHOICES = (
        ("service", u"Обслуговування"),
        ("menu", u"Меню"),
        ("bill", u"Рахунок"),
        ("check", u"Чек")
    )
    FEED_BOOK_CHOICES = (
        ("nothing", u"Без ЗАпису до книги"),
        ("added", u"Зроблено запис у книги про вказані порушення"),
        ("none", u"Відсутня книга відгуків"),
        ("refuse", u"Відмовились надати книгу відгуків"),
    )

    place = models.ForeignKey(Place)
    no_ukr = models.CharField(choices=NO_UKR_CHOICES, max_length=100)
    feedback_book = models.CharField(choices=FEED_BOOK_CHOICES, max_length=100)
    date = models.DateField(default=datetime.date.today)