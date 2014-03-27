# -*- coding: utf-8 -*-
from datetime import date, timedelta

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin, BaseUserManager)
from django.template import defaultfilters as filters
from django.conf import settings
from django.core.urlresolvers import reverse

from django_extensions.db.fields import encrypted # http://goo.gl/WVCZV1


# Create your models here.

class TypeOfItem(models.Model):
    kor = models.CharField(max_length=254)
    _eng = models.CharField(max_length=254)

    @property
    def eng(self):
        return self._eng.capitalize()

    def __unicode__(self):
        return self._eng

    def get_absolute_url(self):
        return reverse('type_of_item-detail', args=[str(self.id)])

class ItemBox(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL)
    items = models.ManyToManyField(TypeOfItem,)

    def __unicode__(self):
        return self.owner.name + _("'s item_box.")

class Item(models.Model):
    kor = models.CharField(max_length=254)
    _eng = models.CharField(max_length=254)
    number_of_elem = models.PositiveSmallIntegerField()

    form = models.ForeignKey(TypeOfItem, related_name='items')

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    @property
    def eng(self):
        return self._eng.capitalize()

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.form._eng), str(self.id)])

    def __unicode__(self):
        return filters.truncatechars(self.kor+"("+self.eng+")", 30)

class Category(models.Model):
    name = models.CharField(max_length=254)

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __unicode__(self):
        return self.name

class Question(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='questions')
    contents = models.TextField()
    category = models.ForeignKey(Category, related_name='questions')

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse(
            'question-detail',
            args=[
                str(self.id),
            ],
        )

    def date_of_receive(self):
        try:
            return self.answers.first().creation.date()
        except AttributeError:
            return None
        except:
            assert False, 'error'

    @property
    def owner(self):
        return self.writer

    def __unicode__(self):
        return filters.truncatechars(self.contents, 30)

class Answer(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers')
    contents = encrypted.EncryptedTextField()
    question = models.ForeignKey(Question, related_name='answers')

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    @property
    def owner(self):
        return self.writer

    def get_absolute_url(self):
        return reverse(
            'answer-detail',
            args=[
                str(self.question.id),
                str(self.id)
            ],
        )

    def __unicode__(self):
        return filters.truncatechars(self.contents, 30)

class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='activity_log')
    question = models.ForeignKey(Question, related_name='activity_log')
    item = models.ForeignKey(Item, related_name='activity_log')

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    @property
    def owner(self):
        return self.user

    def get_absolute_url(self):
        return reverse('activity_log-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'ActivityLog'

class MyUserManager(BaseUserManager):
    def create(self, email, name, birthday, sex, password):
        return self.create_user(email=email,
                                password=password,
                                name=name,
                                birthday=birthday,
                                sex=sex,
        )

    def create_user(self, email, name, birthday, sex, password):
        if not email:
            raise ValueError(_('email cannot be blank.'))
 
        user = self.model(
            email=MyUserManager.normalize_email(email),
            name=name,
            birthday=birthday,
            sex=sex,
            is_active=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, name, birthday, sex, password):
        user = self.create_user(email=email,
            password=password,
            name=name,
            birthday=birthday,
            sex=sex,
        )
        user.is_staff=True
        user.is_superuser=True
        user.is_admin=True
        user.save(using=self._db)

        return user

class VomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    name = models.CharField(max_length=254)
    birthday = models.DateField()
    sex = models.SmallIntegerField()

    date_of_receving_last_question = models.DateField(
        default=date.today()-timedelta(days=1)
    )
    question_of_today = models.ForeignKey(Question, null=True, blank=True)
    # constellation = models.ForeignKey(Constellation, null=True, blank=True)
    switch = models.BooleanField(default=False)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    creation = models.DateTimeField(auto_now_add=True)
    modification = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    is_staff = models.BooleanField(default=False, blank=True,)
    is_active = models.BooleanField(default=True, blank=True,)

    def get_absolute_url(self):
        return reverse('accounts')

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return super(VomUser, self).has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return super(VomUser, self).has_module_perms(app_label)

    def get_short_name(self):
        return self.name

    def get_username(self):
        return self.name

    def get_full_name(self):
        return self.name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birthday', 'sex', ]

