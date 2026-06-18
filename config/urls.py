from django.contrib import admin
from django.urls import path, include
from board.views import base_views
from common.views import account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),
    path('reset/<uidb64>/<token>/', account_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # 추가
    path('accounts/', include('allauth.urls')),  # allauth URL 추가
]

handler404 = 'common.views.common_views.page_not_found'