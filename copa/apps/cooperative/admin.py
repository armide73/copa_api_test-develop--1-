from django.contrib import admin
from .models import Cooperative, Member, \
    MemberMeta, CooperativeMeta, MemberField, CooperativeEmployee

# Register your models here.
admin.site.register(Cooperative)
admin.site.register(Member)
admin.site.register(CooperativeMeta)
admin.site.register(MemberMeta)
admin.site.register(MemberField)
admin.site.register(CooperativeEmployee)
