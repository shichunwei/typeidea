# -*- coding = utf-8 -*-
# @Time    : 2023/11/21 15:37
# @Author  : ShiChunWei
"""Form是对用户输入以及Model中要展示数据的抽象"""
from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
