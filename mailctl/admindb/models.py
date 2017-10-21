# This Python file uses the following encoding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#from mail.lib.db.models.fields import FQDNField
from lib.db.models import fields
#from django.forms import ComboField
#from admindb.form import PasswdField

class   Domains        (models.Model):
    """
    Mail domain, fqdn
    """
    DOMAIN_TYPES = (    (u'VIRTUAL',    u'Виртуальный домен'),
                        (u'LOCAL',      u'Локальный домен'),
                        (u'RELAY',      u'Домен, разрешенный для пересылки (Relay domain)'),
                    );
    domain      = fields.FQDNField  (max_length     = 128,
                                     verbose_name   = "Почтовый домен",
                                     help_text      = "Полное имя почтового домена (fqdn)",
                                     primary_key    = True)
    type        = models.CharField  (max_length     = 10,
                                     verbose_name   = "Тип домена",
                                     choices        = DOMAIN_TYPES,
                                     default        = 'VIRTUAL')
    comment   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     verbose_name   = "Comment",
                                     help_text      = "Комментарий")
    class Meta:
        verbose_name = "Почтовый домен"
        verbose_name_plural = "Почтовые домены"
        ordering = ['domain']

    def __unicode__(self):
        return self.domain

class   Aliases    (models.Model):
    """
    Mail aliases
    """
    localpart   = models.CharField  (max_length     = 64,
                                     verbose_name   = "Alias localpart",
                                     help_text      = "Имя пользователя псевдонима")
    domain      = models.ForeignKey (Domains,
                                     verbose_name   = "Alias domain",
                                     help_text      = "Домен псевдонима")
    recipients  = models.TextField  (verbose_name   = "Получатели",
                                     help_text      = "Список получателей, разделенный запятыми")
    comment   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     verbose_name   = "Comment",
                                     help_text      = "Комментарий")
    class Meta:
        unique_together = (("localpart", "domain"),)
        verbose_name = "Псевдоним"
        verbose_name_plural = "Псевдонимы"
        ordering = ['domain', 'localpart']
#        ordering = ['localpart', 'domain']

    def __unicode__(self):
        return self.localpart + "@" + self.domain.domain + " => " + self.recipients

class   Forwards    (models.Model):
    """
    Advanced mail aliases (see exim conf)
    """
    localpart   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     default        = '',
                                     verbose_name   = "Alias localpart",
                                     help_text      = "Имя пользователя псевдонима")
    domain      = fields.FQDNField  (max_length     = 128,
                                     blank          = True,
                                     default        = '',
                                     verbose_name   = "Alias domain",
                                     help_text      = "Домен псевдонима")
    recipient_localpart = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     default        = '',
                                     verbose_name   = "Recipient localpart",
                                     help_text      = "Имя пользователя получателя")
    recipient_domain = fields.FQDNField  (max_length     = 128,
                                     verbose_name   = "Recipient domain",
                                     help_text      = "Домен получателя")
    priority    = models.IntegerField  (verbose_name   = "Приоритет",
                                     default        = 0,
                                     help_text      = "Приоритет псевдонима, для доставки почты будет использоваться псевдоним с максимальным приориотетом")
    comment   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     verbose_name   = "Comment",
                                     help_text      = "Комментарий")
    class Meta:
        unique_together = (("localpart", "domain", "recipient_localpart", "recipient_domain", "priority"),)
        verbose_name = "Улучшенный псевдоним"
        verbose_name_plural = "Улучшенные псевдонимы"
        ordering = ['localpart', 'domain']

    def __unicode__(self):
        return self.localpart + "@" + self.domain + " => " + self.recipient_localpart + "@" + self.recipient_domain

class Users        (models.Model):
    """
    Virtual mail users
    """
    localpart   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     default        = '',
                                     verbose_name   = "Имя пользователя")
    domain      = models.ForeignKey (Domains,
                                     default        = 'fakedomain.tld',
                                     verbose_name   = "Домен")
    PLAIN = '{PLAIN}'
    CRYPT = '{CRYPT}'
    READY = '{READY}'
    CRYPT_CHOICES = ((READY,'{READY}'),(PLAIN,'{PLAIN}'),(CRYPT,'{CRYPT}'))
    crypto      = models.CharField (max_length      = 10,
                                    default         = READY,
                                    choices         = CRYPT_CHOICES,
                                    verbose_name    = "Кодировать")
    passwd      = models.CharField (max_length      = 32,
                                    default         = '',
                                    blank           = False,
                                    verbose_name    = "Пароль")
    quota       = models.IntegerField (verbose_name = "Квота",
                                     default        = 500,
                                     help_text      = "Дисковая квота в МБ (0 - для неограниченного ящика)")
    enabled     = models.BooleanField (verbose_name = "Активен",
                                     default        = True,
                                     help_text      = "Активирует доставку почты для пользователя")
    remote_access = models.BooleanField (verbose_name = "Удаленный доступ",
                                     default        = False,
                                     help_text      = "Активирует работу с почтой из нелокальных сетей")
    comment   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     verbose_name   = "Comment",
                                     help_text      = "Комментарий")
    class Meta:
        verbose_name = "Пользователь почты"
        verbose_name_plural = "Пользователи почты"
        unique_together = (("localpart", "domain"),)
        ordering = ['localpart', 'domain']

    def is_upperclass(self):
        return self.crypto in (self.PLAIN, self.CRYPT)

    def __unicode__(self):
        return self.localpart + "@" + self.domain.domain

    def generate_hash_password(self):
        return "%s%s" % (self.crypto, self.passwd)

class Masters        (models.Model):
    """
    Mail users masters
    """
    user   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     unique         = True,
                                     default        = '',
                                     verbose_name   = "Имя суперпользователя")
    PLAIN = '{PLAIN}'
    CRYPT = '{CRYPT}'
    READY = '{READY}'
    CRYPT_CHOICES = ((READY,'{READY}'),(PLAIN,'{PLAIN}'),(CRYPT,'{CRYPT}'))
    crypto      = models.CharField (max_length      = 10,
                                    default         = READY,
                                    choices         = CRYPT_CHOICES,
                                    verbose_name    = "Кодировать")
    passwd      = models.CharField (max_length      = 32,
                                    default         = '',
                                    blank           = False,
                                    verbose_name    = "Пароль")
    enabled     = models.BooleanField (verbose_name = "Активен",
                                     default        = True,
                                     help_text      = "Активирует пользователя")
    comment   = models.CharField  (max_length     = 64,
                                     blank          = True,
                                     verbose_name   = "Comment",
                                     help_text      = "Комментарий")
    class Meta:
        verbose_name = "Суперпользователь почты"
        verbose_name_plural = "Суперпользователи почты"
        ordering = ['user']

    def is_upperclass(self):
        return self.crypto in (self.PLAIN, self.CRYPT)

#    def __unicode__(self):
#        return self.user

    def generate_hash_password(self):
        return "%s%s" % (self.crypto, self.passwd)

from django.db.models.signals import pre_save
from django.core.signals import request_finished
from django.dispatch import receiver
#from django.contrib.auth.hashers import make_password
import random
import crypt

@receiver(pre_save, sender=Users)
@receiver(pre_save, sender=Masters)
def crypt_password(sender, instance, **kwargs):
     if instance.crypto=='{CRYPT}':
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        instance.passwd = instance.crypto + crypt.crypt(instance.passwd, ''.join(random.choice(ALPHABET) for i in range(10)))
        instance.crypto = '{READY}'
     elif instance.crypto=='{PLAIN}':
        instance.passwd = instance.generate_hash_password()
        instance.crypto = '{READY}'
