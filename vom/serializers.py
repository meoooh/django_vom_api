from django.utils.translation import ugettext as _

from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.Field(source="get_absolute_url")

    class Meta:
        model = Category

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate_current_password(self, attrs, source):
        # http://goo.gl/5Frj9Z
        if not self.object.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                _("Current password is not correct"),
                code='password_wrong',
            )

        return attrs

    def validate_new_password2(self, attrs, source):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError(
                _("This field must be matched by password field."),
                code='password_mismatch',
            )

        return attrs

    def restore_object(self, attrs, instance=None):
        """ change password """
        if instance is not None:
            instance.set_password(attrs['new_password2'])
            return instance
        
        return VomUser(**attrs)

class UserCreationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    url = serializers.Field(source="get_absolute_url")

    class Meta:
        model = VomUser
        fields = ('url', 'id', 'email', 'sex', 'birthday',
                  'name', 'password', 'password2', 'creation', 'modification')
        # read_only_fields = ('email', 'creation')
        write_only_fields = ('password',)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(UserCreationSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def restore_object(self, attrs, instance=None):
        user = super(UserCreationSerializer, self).restore_object(attrs, instance)
        if instance is None:
            user.set_password(attrs['password'])
        return user

    def to_native(self, obj):
        if 'password2' in self.fields:
            del self.fields['password2']
        return super(UserCreationSerializer, self).to_native(obj)

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
        if attrs.get('password') == attrs.pop('password2'):
            return attrs
        raise serializers.ValidationError(
            _("This field must be matched by password field."),
            code='password_mismatch',
        )

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()
    url = serializers.Field(source="get_absolute_url")

    class Meta:
        model = VomUser
        fields = ('url', 'id', 'email', 'sex', 'birthday',
                  'name', 'password', 'password2', 'creation', 'modification')
        read_only_fields = ('email',)
        write_only_fields = ('password',)

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

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if instance is None:
            user.set_password(attrs['password'])
        return user

    def to_native(self, obj):
        if 'password2' in self.fields:
            del self.fields['password2']
        return super(UserSerializer, self).to_native(obj)

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
        if attrs.get('password') == attrs.pop('password2'):
            return attrs
        raise serializers.ValidationError(
            _("This field must be matched by password field."),
            code='password_mismatch',
        )

class ItemSerializer(serializers.ModelSerializer):
    url = serializers.Field(source="get_absolute_url")
    form = serializers.Field(source="form")

    class Meta:
        model = Item

class QuestionSerializer(serializers.ModelSerializer):
    url = serializers.Field(source="get_absolute_url")
    date_of_receive = serializers.Field(source="date_of_receive")

    class Meta:
        model = Question
        fields = ('url', 'id', 'contents', 'date_of_receive',)

class AnswerSerializer(serializers.ModelSerializer):
    url = serializers.Field(source="get_absolute_url")
    writer = serializers.Field(source='writer')

    class Meta:
        model = Answer
        fields = ('url', 'id', 'question', 'writer', 'contents', 'creation',
                'modification',)
        read_only_fields = ('question',)

class AnswerCreationSerializer(serializers.ModelSerializer):
    url = serializers.Field(source="get_absolute_url")
    writer = serializers.Field(source='writer')

    class Meta:
        model = Answer
        fields = ('url', 'id', 'question', 'writer', 'contents', 'creation',
                'modification')
        read_only_fields = ('question',)

    # def validate(self, attrs):
    #     import ipdb; ipdb.set_trace()
    #     pass
