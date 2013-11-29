from django.utils.translation import ugettext as _

from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Question


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = VomUser
        fields = ('id', 'email', 'sex', 'birthday',
                  'name', 'password', 'password2')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(UserSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_password_field(self, model_field):
        return None

    def get_password2_field(self, model_field):
        return None

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if instance is None:
            user.set_password(attrs['password'])
        return user

    def to_native(self, obj):
        pass

    def validate_sex(self, attrs, source):
        if attrs['sex'] not in (0, 1):
            raise serializers.ValidationError(
                _("You must choice '1' or '0'. '1' means male and '0' means" +
                    " female. Your input: '%(value)s'"),
                code='invalid',
                params={'value': attrs['sex']}
            )
        return attrs

    def validate_password2(self, attrs, source):
        # http://goo.gl/U7FGWZ
        if attrs['password'] == attrs.pop('password2'):
            return attrs
        raise serializers.ValidationError(
            _("The two password fields didn't match."),
            code='password_mismatch',
        )

    # def save_object(self, obj, **kwargs):
    #     user = super(UserSerializer, self).save_object(obj, **kwargs)
    #     user.set_password(seri)
    #     if commit:
    #         user.save()
    #     return user


class AnswerSerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ('id', 'question', 'writer', 'contents',)
