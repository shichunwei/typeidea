from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import Post, Category, Tag
from .adminforms import PostAdminForm


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 展示列表
    list_display = ('name', 'status', 'is_nav', 'owner', 'post_count', 'created_time')

    # 创建列表(编辑列表)
    fields = ('name', 'status', 'is_nav')

    # 过滤器
    list_filter = ['name', ]
    search_fields = ['name', ]

    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        # 自动保存为当前登录作者
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 展示列表筛选 -- 只展示当前用户分类
        qs = super(CategoryAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')

    fields = ('name', 'status')

    # 过滤器
    list_filter = ['name', ]
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 展示列表筛选 -- 只展示当前用户标签
        qs = super(TagAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def __str__(self):
        return self.name


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 展示列表筛选 -- 只展示当前用户文章
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

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
