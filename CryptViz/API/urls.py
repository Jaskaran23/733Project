from rest_framework import routers
from API.api import PageDetail, PageList

urlpatterns = []

router = routers.DefaultRouter()
router.register('page','page', PageDetail.as_view)
router.register('page','pages', PageList.as_view)
#  urlpatterns += router.urls
