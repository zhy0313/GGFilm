# -*- coding: utf-8 -*-
from django.db import models


class FilmSearch(models.Model):
    Film = models.CharField('Film', max_length=100, db_index=True)
    Developer = models.CharField('Developer', max_length=100, db_index=True)
    Dilution = models.CharField('Dilution', max_length=100, db_index=True)
    ASA_ISO = models.CharField('ASA/ISO', max_length=100, db_index=True)
    a35mm = models.CharField('a35mm', max_length=100)
    a120 = models.CharField('a120', max_length=100)
    Sheet = models.CharField('Sheet', max_length=100)
    Temp = models.CharField('Temp', max_length=100)
    Notes = models.CharField('Notes', max_length=100)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Film

    class Meta:
        verbose_name = "Massive Dev Chart"
        verbose_name_plural = "Massive Dev Chart"


class Films(models.Model):
    Film = models.CharField('Film', max_length=100)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Film

    class Meta:
        verbose_name = "Films"
        verbose_name_plural = "Films"


class Developers(models.Model):
    Developer = models.CharField('Developer', max_length=100)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Developer

    class Meta:
        verbose_name = "Developers"
        verbose_name_plural = "Developers"


class Notes(models.Model):
    Notes = models.CharField('Notes', max_length=100)
    Remark = models.CharField('Remark', max_length=200)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Notes

    class Meta:
        verbose_name = "Notes' Remark"
        verbose_name_plural = "Notes' Remark"


class TempItemStorage(models.Model):
    ItemLink = models.URLField(u'商品URL地址')
    ItemPicId = models.CharField(u'商品展示图ID', max_length=200)
    ItemTitle = models.CharField(u'商品描述', max_length=500)
    ItemShopName = models.CharField(u'店铺名', max_length=200)
    ItemLocation = models.CharField(u'商品来源地', max_length=100)
    ItemPrice = models.CharField(u'商品价格', max_length=100)
    ItemTaoBaoPrice = models.CharField(u'商品淘宝价格', max_length=100)
    ItemDeal = models.CharField(u'商品交易量', max_length=100)
    Has_Been_Selected = models.BooleanField(u'是否加入价格跟踪队列', default=False)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ItemPicId

    class Meta:
        verbose_name = "Temporary Item Storage"
        verbose_name_plural = "Temporary Item Storage"


class ItemStorage(models.Model):
    ItemLink = models.URLField(u'商品URL地址')
    ItemTitle = models.CharField(u'商品描述', max_length=500)
    ItemShopName = models.CharField(u'店铺名', max_length=200)
    ItemPrice = models.CharField(u'商品价格', max_length=100)
    ItemTaoBaoPrice = models.CharField(u'商品淘宝价格', max_length=100)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ItemTitle

    class Meta:
        verbose_name = "Item Storage"
        verbose_name_plural = "Item Storage"
