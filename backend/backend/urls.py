from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from .views import SearchView, article_infos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # ton app
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/similar/', SearchView.as_view(), name='similar'),
    path('api/article_infos/', article_infos, name='article_infos'),
    
]+ static('/images/', document_root=settings.EXTRA_IMAGE_DIR)
