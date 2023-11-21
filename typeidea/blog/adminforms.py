# -*- coding = utf-8 -*-
# @Time    : 2023/11/21 15:37
# @Author  : ShiChunWei
from django import forms


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
