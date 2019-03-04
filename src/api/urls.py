from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from .views import MoviesView#, CommentsView, TopView

router = SimpleRouter()
router.register(r'movies', MoviesView)
# router.register(r'comments', CommentsView)
# router.register(r'top', TopView)

urlpatterns = router.urls
