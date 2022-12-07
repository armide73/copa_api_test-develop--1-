"""copa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # noqa
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .apps.cooperative.views import UploadMembers, \
    UploadMemberImage
from .apps.stock.views import UploadProductivity
from copa.apps import spenn

admin.site.site_header = 'COPA Admin'
admin.site.site_title = 'COPA Admin Portal'
admin.site.index_title = 'Welcome to COPA Admin Portal'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('copa/v1/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('copa/v1/upload/members/<id>', UploadMembers.as_view(),
         name="upload_members"),
    path('copa/v1/upload/member/profile/<id>', UploadMemberImage.as_view(),
         name="upload_member_image"),
    path('copa/v1/upload/productivity/<id>', UploadProductivity.as_view(),
         name="upload_member_image"),
    # path('ledger/', include('django_ledger.urls',
    #      namespace='django_ledger')),
    path('copa/v1/', include('copa.apps.spenn.urls')),
]
