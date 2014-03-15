# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.db.models import Q

from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action

from vom import models, serializers, custom_permissions

class UserCreationSet(generics.CreateAPIView):
    """신규 사용자 생성"""
    serializer_class = serializers.UserCreationSerializer
    model = models.VomUser

class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    model = models.VomUser
    serializer_class = serializers.UserSerializer
    permission_classes = (custom_permissions.permissions.IsAuthenticated,
                        custom_permissions.IsOwner,)

    def retrieve(self, request, *args, **kwargs):
        """내 정보 가져오기"""
        return super(UserDetailViewSet, self).retrieve(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

class AnswerCreationSet(generics.ListCreateAPIView):
    serializer_class = serializers.AnswerCreationSerializer
    # model  = models.Answer
    permission_classes = (custom_permissions.permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Answer.objects.filter(
            writer=self.request.user,
            question=self.kwargs['question_pk'],
        )

        return queryset

    # def create(self, request, *args, **kwargs):
    #     import ipdb; ipdb.set_trace()
    #     serializer = self.get_serializer_class()
    #     data = dict(request.DATA)
    #     data['question'] = [self.kwargs.get('question_pk')]
    #     serializer = serializer(data=request.DATA)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, 
    #                         status=status.HTTP_400_BAD_REQUEST)

class AnswerDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AnswerSerializer
    # queryset  = models.Answer.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated,
                            custom_permissions.IsOwner,)

    def get_queryset(self):
        q = Q(writer=self.request.user)
        q = q & Q(question__pk=self.kwargs['question_pk'])

        return models.Answer.objects.filter(q)

    def pre_save(self, obj):
        obj.writer = self.request.user

    # def get_object(self):
    #     pass

    # def get_queryset(self):
    #     # import ipdb; ipdb.set_trace()
    #     queryset  = models.Answer.objects.get(
    #         writer__id=self.kwargs['user_pk'],
    #         question__id=self.kwargs['question_pk']
    #     )

    #     return queryset


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset  = models.Question.objects.all()
    # permission_classes = (custom_permissions.permissions.IsAuthenticated)

    def get_queryset(self):
        q = Q(answers__writer=self.request.user)
        queryset  = models.Question.objects.filter(q).distinct()

        return queryset

    # @action()
    # def answers(self, request, pk=None):
    #     import ipdb; ipdb.set_trace()
    #     answer = models.Answer(
    #         writer=request.user,
    #         contents=request.DATA.get('contents', None),
    #         question=self.get_object()
    #     )
    #     answer.save()
    #     serializer = serializers.AnswerSerializer(answer)

    #     return Response(serializer.data, status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset  = models.Category.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated)

class ConstellationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ConstellationSerializer
    queryset  = models.Constellation.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    queryset  = models.Item.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated)

@api_view(['PATCH'])
@permission_classes((custom_permissions.permissions.IsAuthenticated, ))
def changePassword(request):
    """
    비밀번호 변경

    current_password -- 현재 비밀번호
    new_password -- 변경할 비밀번호
    new_password2 -- 변경할 비밀번호(확인)
    """
    serializer = serializers.ChangePasswordSerializer(request.user,
                                                    request.DATA,)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
