# -*- coding: utf-8 -*-
from datetime import date

from django.utils.translation import ugettext as _
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import Http404

from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action

from vom import models, serializers, custom_permissions

class UserCreationSet(generics.CreateAPIView):
    """신규 사용자 생성"""
    serializer_class = serializers.UserCreationSerializer
    model = models.VomUser

    def post_save(self, obj, created=False):
        toi = models.TypeOfItem.objects.first()
        assert toi, 'There is no TypeOfItem.'

        models.ItemBox.objects.create(owner=obj).items.add(toi)

        item = models.Item.objects.order_by('?').first()
        assert item, 'There is no Item.'

        obj.item_which_I_am_collecting = item
        obj.save()


class UserDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """내 정보"""
    model = models.VomUser
    serializer_class = serializers.UserSerializer
    permission_classes = (custom_permissions.permissions.IsAuthenticated,
                        custom_permissions.IsOwner,)

    def retrieve(self, request, pk=None):
        """내 정보 가져오기"""
        return super(UserDetailViewSet, self).retrieve(request, pk)

    # update, partial_update시 password는 변경하지 않도록 처리햐야함...
    # def update(self, request, pk=None):
    #     import ipdb; ipdb.set_trace()

    # def partial_update(self, request, pk=None):
    #     pass

    def get_object(self):
        return self.request.user

class AnswerCreationSet(generics.ListCreateAPIView):
    """답변 목록 및 답변 등록"""
    serializer_class = serializers.AnswerCreationSerializer
    # model  = models.Answer
    permission_classes = (custom_permissions.permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Answer.objects.filter(
            writer=self.request.user,
            question=self.kwargs['question_pk'],
        )

        return get_list_or_404(queryset)

    def get_object(self):
        pass

    def pre_save(self, obj):
        obj.writer = self.request.user
        try:
            obj.question = models.Question.objects.get(
                pk=self.kwargs['question_pk']
            )
        except models.Question.DoesNotExist:
            raise Http404

    def post_save(self, obj, created=False):
        pass

class AnswerDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    """나의 답변"""
    serializer_class = serializers.AnswerSerializer
    # queryset  = models.Answer.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated,
                            custom_permissions.IsOwner,)

    def get_queryset(self):
        q = Q(writer=self.request.user)
        q = q & Q(question__pk=self.kwargs['question_pk'])

        queryset = models.Answer.objects.filter(q)
        if queryset:
            return queryset
        else:
            raise Http404

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
    """내가 답변한 질문"""
    serializer_class = serializers.QuestionSerializer
    queryset  = models.Question.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated, )

    def get_queryset(self):
        queryset  = models.Question.objects.filter(
            answers__writer=self.request.user).distinct()
        queryset = sorted(queryset, key=lambda qs: qs.date_of_receive())

        return queryset

    def get_object(self):
        queryset  = models.Question.objects.filter(
            answers__writer=self.request.user
        ).distinct()

        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    # @action()
    # def answers(self, request, pk=None):
    #     import ipdb; ipdb.set_trace()
    #     data = dict(request.DATA)
    #     data['question'] = pk
    #     # data['writer']
    #     serializer = serializers.AnswerSerializer(data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset  = models.Category.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated,)

class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ItemSerializer
    queryset  = models.Item.objects.all()
    permission_classes = (custom_permissions.permissions.IsAuthenticated,)

    def pk_list_or_404(self):
        item_name = self.kwargs['item_name']
        toi = get_object_or_404(models.TypeOfItem, _eng=item_name)
        if self.request.user.itembox.items.filter(pk=toi.pk).exists():
            al = models.ActivityLog.objects.filter(
                user=self.request.user
                ).values_list('item', flat=True)
        else:
            raise Http404

        return al

    def get_queryset(self):
        queryset = get_list_or_404(models.Item, pk__in=self.pk_list_or_404())

        return queryset

    def get_object(self):
        if int(self.kwargs['pk']) not in self.pk_list_or_404():
            raise Http404
        return get_object_or_404(models.Item, pk=self.kwargs['pk'])

class QuestionRelatedItemViewSet(generics.ListAPIView):
    serializer_class = serializers.QuestionSerializer
    permission_classes = (custom_permissions.permissions.IsAuthenticated,)

    def get_queryset(self):
        item_name = self.kwargs['item_name']
        item_pk = self.kwargs['item_pk']

        toi = get_object_or_404(models.TypeOfItem, _eng=item_name)

        if self.request.user.itembox.items.filter(pk=toi.pk).exists():
            item = get_object_or_404(models.Item, pk=item_pk, form=toi)
            al = models.ActivityLog.objects.filter(
                user=self.request.user, item=item
            ).values_list('question', flat=True)
            queryset = get_list_or_404(models.Question, pk__in=al)
            queryset = sorted(queryset, key=lambda qs: qs.date_of_receive())
        else:
            raise Http404

        return queryset

@api_view(['PATCH'])
@permission_classes((custom_permissions.permissions.IsAuthenticated,))
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

def get_question_of_today(request):
    if request.user.date_of_receving_last_question < date.today():
        try:
            question = models.Question.objects.exclude(
                answers__writer=request.user).order_by('?')[0]
        except IndexError:
            assert False, "There is no loger question."
        request.user.question_of_today = question
        request.user.date_of_receving_last_question = date.today()
        request.user.is_register_first_answer = False

        number_of_item = models.ActivityLog.objects.filter(
            user=request.user,
            item=request.user.item_which_I_am_collecting
        ).count()
        number_of_iwIac = request.user.item_which_I_am_collecting.number_of_elem

        if number_of_item == number_of_iwIac:
            pk_list_of_item = models.ActivityLog.objects.filter(
                user=request.user,
            ).values_list('item', flat=True)

            q = Q(pk__in=pk_list_of_item)
            q = q & ~Q(form=request.user.itembox.items.last())

            excluded_items = models.Item.objects.exclude(q)
            print excluded_items
            new_item = excluded_items.order_by('?').first()

            assert new_item, "There is no longer item."

            request.user.item_which_I_am_collecting = new_item

        request.user.save()
    else:
        question = request.user.question_of_today

    return question

@api_view(['GET'])
@permission_classes((custom_permissions.permissions.IsAuthenticated,))
def question_of_today(request):
    """
    오늘의 질문 보기
    """
    question = get_question_of_today(request)

    serializer = serializers.QuestionSerializer(question)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((custom_permissions.permissions.IsAuthenticated,))
def answer_question_of_today(request):
    """
    오늘의 질문에 대한 답변 등록하기

    contents -- 답변 내용
    """
    question = get_question_of_today(request)
    serializer = serializers.AnswerSerializer(data=request.DATA)

    if not serializer.is_valid():
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    serializer.object.writer = request.user
    serializer.object.question = request.user.question_of_today
    serializer.save()
    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    response['Location'] = reverse(
        'answer-detail',
        args=[
            serializer.data['question'],
            serializer.data['id'],
        ],
    )

    if not request.user.is_register_first_answer:
        models.ActivityLog.objects.create(
            user=request.user,
            question=question,
            item=request.user.item_which_I_am_collecting
        )
        request.user.is_register_first_answer = True
        request.user.save()

    return response

@api_view(['DELETE'])
@permission_classes((custom_permissions.permissions.IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
