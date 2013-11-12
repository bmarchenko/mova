#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from django.contrib.gis.db import models
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse


class Map(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Карта"
        verbose_name_plural = "Карти"

    def get_absolute_url(self):
        return reverse('map', args=[self.slug])


class Region(models.Model):
    title = models.CharField(max_length=200, verbose_name=u"Назва")
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Регіон"
        verbose_name_plural = "Регіони"


class Place(models.Model):
    TYPE_CHOICES = (
        ("lang-shop", u"Магазин"),
        ("lang-cafe", u"Заклад Харчування"),
        ("lang-pharmacy", u"Aптека"),
        ("lang-gasstation", u"АЗС")
    )
    COLOR_CHOICES = (
        (1, u"червоний"),
        (2, u"жовтий"),
        (3, u"зелений")
    )

    title = models.CharField(max_length=200, verbose_name=u"Назва закладу")
    address = models.CharField(max_length=2000, verbose_name=u"Адреса")
    owner = models.CharField(max_length=200, verbose_name=u"Власник закладу")
    slug = AutoSlugField(populate_from="title")
    color = models.IntegerField(choices=COLOR_CHOICES, verbose_name=u"Колір")
    type = models.CharField(choices=TYPE_CHOICES, max_length=100, verbose_name=u"Тип закладу")
    region = models.ForeignKey(Region, verbose_name=u"Регіон")
    geometry = models.PointField(srid=4326, blank=True, null=True)
    map_geo = models.ForeignKey(Map, blank=True, null=True, verbose_name=u"Карта")
    objects = models.GeoManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.geometry:
            self.geocoded = True
        super(Place, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Місце"
        verbose_name_plural = "Місця"
        ordering = ['title']


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, u"Чоловіча"),
        (2, u"Жіноча")
    )
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name=u"Стать")
    name = models.CharField(max_length=200, verbose_name=u"ПІБ")
    address = models.CharField(max_length=500, verbose_name=u"Адреса")
    email = models.EmailField()
    phone = models.IntegerField(verbose_name=u"Телефон")

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"


class Poll(models.Model):

    FEED_BOOK_CHOICES = (
        ("nothing", u"Без запису до книги"),
        ("added", u"Зроблено запис у книги про вказані порушення"),
        ("none", u"Відсутня книга відгуків"),
        ("refuse", u"Відмовились надати книгу відгуків"),
    )

    place = models.ForeignKey(Place)
    service = models.BooleanField(verbose_name=u"Обслуговування")
    menu = models.BooleanField(verbose_name=u"Меню")
    bill = models.BooleanField(verbose_name=u"Рахунок")
    check = models.BooleanField(verbose_name=u"Чек")
    feedback_book = models.CharField(choices=FEED_BOOK_CHOICES, max_length=100, verbose_name=u"Книга відгуків")
    date = models.DateField(default=datetime.date.today, verbose_name=u"Дата")
    user = models.ForeignKey(Profile, verbose_name=u"Користувач")
    approved = models.BooleanField(default=False, verbose_name=u"Підтверджено")

    def __unicode__(self):
        return u"{0} - {1}".format(self.place.title, self.user.name)


    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"



