from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register('type', views.TypeListGenericView)
router.register('food', views.FoodListGenericView)
router.register('comment', views.CommentListMixinView)
router.register('favorite', views.FavoriteListMixinView)

app_name = 'food'
urlpatterns = router.urls
