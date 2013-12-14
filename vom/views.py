from rest_framework import generics, permissions, viewsets, mixins

from vom import models, serializers

class UserViewSet(viewsets.ModelViewSet):
    """test"""
    serializer_class = serializers.UserSerializer
    queryset  = models.VomUser.objects.all()
    # permission_classes = (permissions.DjangoModelPermissions,)
    paginate_by = 10
    pagination_serializer_class = serializers.UserPaginationSerializer
