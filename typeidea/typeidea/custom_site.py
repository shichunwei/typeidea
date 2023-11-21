# -*- coding = utf-8 -*-
# @Time    : 2023/11/21 15:53
# @Author  : ShiChunWei
from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea管理后台'
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
