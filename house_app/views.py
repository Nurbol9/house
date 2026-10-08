from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import PropertyFilter
from .models import Property, Review, UserProfile
from .permission import IsPropertyOwnerOrReadOnly, IsReviewAuthorOrReadOnly
from .serializers import (
    LoginSerializer,
    PropertyDetailSerializer,
    PropertyListSerializer,
    ReviewDetailSerializer,
    ReviewListSerializer,
    UserProfileSerializer,
    UserSerializer,
)


# ---------- Auth ----------

class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)




class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.select_related('seller').prefetch_related('images')
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'region', 'city', 'district', 'address']
    ordering_fields = ['price', 'area', 'created_at']
    ordering = ['-created_at']


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.select_related('seller').prefetch_related('images')
    serializer_class = PropertyDetailSerializer
    permission_classes = [IsPropertyOwnerOrReadOnly]


# ---------- Review ----------

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.select_related('author', 'seller')
    serializer_class = ReviewListSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related('author', 'seller')
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]