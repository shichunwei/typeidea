from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

# Register your models here.
from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


class CategoryOwnerFilter(admin.SimpleListFilter):
    # 自定义过滤器自展示当前用户分类
    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            print(category_id)
            return queryset.filter(category_id=category_id)
        return queryset


class PostInline(admin.TabularInline):
    """关联模型编辑"""
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # 关联模型编辑
    inlines = [PostInline, ]

    # 展示列表
    list_display = ('name', 'status', 'is_nav', 'owner', 'post_count', 'created_time')

    # 创建列表(编辑列表)
    fields = ('name', 'status', 'is_nav')

    # 过滤器
    list_filter = ['name', ]
    search_fields = ['name', ]

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def __str__(self):
        return self.name


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')

    fields = ('name', 'status')

    # 过滤器
    list_filter = ['name', ]
    search_fields = ['name', ]

    def __str__(self):
        return self.name


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # 展示页面
    list_display = [
        'title', 'category', 'status', 'owner', 'created_time', 'operator'
    ]
    list_display_links = []

    # 过滤器
    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title']

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ("基础配置", {
            'description': "基础配置描述",
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            )
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    filter_horizontal = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def __str__(self):
        return self.title

    form = PostAdminForm

    # class Media:
    #     """定义页面样式"""
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",
    #                 ),
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    # 日志功能
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
