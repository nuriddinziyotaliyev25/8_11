from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet
from .models import Type, Food, Comment, User, Favorite
from .serializers import TypeSerializer, FoodSerializer, \
    CommentSerializer, RegisterSerializer, \
    FavoriteSerializer
from django.db.models import Q


class TypeListGenericView(ModelViewSet):
    """
    TypeListGenericView:
    Type modeliga oid barcha turdagi API-larni boshqaradi.

    - GET: Turlar ro‘yxatini olish, filtr va tartib bo‘yicha qidirish.
    - POST: Yangi tur qo‘shish.
    - PUT/PATCH: Mavjud tur ma’lumotlarini yangilash.
    - DELETE: Mavjud tur ma’lumotini o‘chirish.
    """
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filtrlash va tartiblashtirishni amalga oshiradi.

        Query parametrlari:
        - `q`: Tur nomi bo‘yicha qidirish.
        - `o`: Tartibni belgilang (e.g., `created_at`, `-created_at`).
        """
        types = Type.objects.all()

        try:
            if self.request.query_params.get('q', False):
                q = self.request.query_params.get('q')
                types = types.filter(Q(title__icontains=q))
        except:
            pass

        try:
            if self.request.query_params.get('o', False):
                types = types.order_by(self.request.query_params.get('o'))
        except:
            pass

        return types


class FoodListGenericView(ModelViewSet):
    """
    FoodListGenericView:
    Food modeliga oid barcha API-larni boshqaradi.

    - GET: Ovqatlar ro‘yxatini olish, filtr va tartib bo‘yicha qidirish.
    - POST: Yangi ovqat qo‘shish.
    - PUT/PATCH: Mavjud ovqat ma’lumotlarini yangilash.
    - DELETE: Mavjud ovqat ma’lumotini o‘chirish.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filtrlash va tartiblashtirishni amalga oshiradi.

        Query parametrlari:
        - `type_id`: Ovqatning turiga ko‘ra filtr.
        - `q`: Ovqat nomi yoki ingredientlari bo‘yicha qidirish.
        - `o`: Tartibni belgilang (e.g., `created_at`, `-created_at`).
        """
        foods = Food.objects.all()

        try:
            if self.request.query_params.get('type_id', False):
                foods = foods.filter(type_id=self.request.query_params.get('type_id'))
        except:
            pass

        try:
            if self.request.query_params.get('q', False):
                q = self.request.query_params.get('q')
                foods = foods.filter(Q(title__icontains=q) | Q(ingredient__icontains=q))
        except:
            pass

        try:
            if self.request.query_params.get('o', False):
                foods = foods.order_by(self.request.query_params.get('o'))
        except:
            pass

        return foods


class CommentListMixinView(ModelViewSet):
    """
    CommentListMixinView:
    Comment modeliga oid barcha API-larni boshqaradi.

    - GET: Kommentariyalar ro‘yxatini olish, filtr va tartib bo‘yicha qidirish.
    - POST: Yangi kommentariya qo‘shish.
    - PUT/PATCH: Mavjud kommentariya ma’lumotlarini yangilash.
    - DELETE: Mavjud kommentariya ma’lumotini o‘chirish.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filtrlash va tartiblashtirishni amalga oshiradi.

        Query parametrlari:
        - `author_id`: Kommentariyaning muallifiga ko‘ra filtr.
        - `food_id`: Kommentariyaning ovqatiga ko‘ra filtr.
        - `q`: Matn bo‘yicha qidirish.
        - `o`: Tartibni belgilang (e.g., `created_at`, `-created_at`).
        """
        comment = Comment.objects.all()

        try:
            if self.request.query_params.get('author_id', False):
                comment = comment.filter(author_id=self.request.query_params.get('author_id'))
        except:
            pass

        try:
            if self.request.query_params.get('food_id', False):
                comment = comment.filter(food_id=self.request.query_params.get('food_id'))
        except:
            pass

        try:
            if self.request.query_params.get('q', False):
                q = self.request.query_params.get('q')
                comment = comment.filter(Q(text__icontains=q))
        except:
            pass

        try:
            if self.request.query_params.get('o', False):
                comment = comment.order_by(self.request.query_params.get('o'))
        except:
            pass

        return comment


class FavoriteListMixinView(ModelViewSet):
    """
    FavoriteListMixinView:
    Favorite modeliga oid barcha API-larni boshqaradi.

    - GET: Sevimli ovqatlar ro‘yxatini olish, filtr va tartib bo‘yicha qidirish.
    - POST: Yangi sevimli qo‘shish.
    - PUT/PATCH: Mavjud sevimli ma’lumotlarini yangilash.
    - DELETE: Mavjud sevimli ma’lumotini o‘chirish.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Filtrlash va tartiblashtirishni amalga oshiradi.

        Query parametrlari:
        - `user_id`: Foydalanuvchiga ko‘ra filtr.
        - `food_id`: Ovqatga ko‘ra filtr.
        - `o`: Tartibni belgilang (e.g., `created_at`, `-created_at`).
        """
        favorites = Favorite.objects.all()

        try:
            if self.request.query_params.get('user_id', False):
                favorites = favorites.filter(user_id=self.request.query_params.get('user_id'))
        except:
            pass

        try:
            if self.request.query_params.get('food_id', False):
                favorites = favorites.filter(food_id=self.request.query_params.get('food_id'))
        except:
            pass

        try:
            if self.request.query_params.get('o', False):
                favorites = favorites.order_by(self.request.query_params.get('o'))
        except:
            pass

        return favorites


class RegisterView(CreateAPIView):
    """
    RegisterView:
    Foydalanuvchini ro‘yxatdan o‘tkazish uchun API.

    - POST: Yangi foydalanuvchi yaratadi va foydalanuvchi ma’lumotlarini qaytaradi.
    """
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    LogoutView:
    Foydalanuvchini tizimdan chiqarish uchun API.

    - POST: Refresh token qabul qiladi va uni qora ro‘yxatga kiritadi, foydalanuvchini tizimdan chiqaradi.
    """

    def post(self, request):
        """
        Refresh tokenni qora ro‘yxatga kiritadi, foydalanuvchini tizimdan chiqaradi.

        - So‘rovda `refresh_token` majburiy. Muvaffaqiyatli bajarilganda `205 Reset Content` statusini qaytaradi.
        """
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': "You are logged out from our site"}, status=205)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
