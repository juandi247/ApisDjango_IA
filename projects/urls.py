from .api import ProjectViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/projects', ProjectViewSet, 'projects')

urlpatterns = router.urls
