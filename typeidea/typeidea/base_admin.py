# -*- coding = utf-8 -*-
# @Time    : 2023/11/21 16:14
# @Author  : ShiChunWei
from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 展示列表筛选 -- 只展示当前用户文章
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
