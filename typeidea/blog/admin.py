from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 展示列表
    list_display = ('name', 'status', 'is_nav', 'owner', 'post_count', 'created_time')
    # 创建列表
    fields = ('name', 'status', 'is_nav')

    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        # 自动保存为当前登录作者
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def __str__(self):
        return self.name


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 展示页面
    list_display = [
        'title', 'category', 'status', 'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = ['category', ]
    search_fields = ['title', 'category_name']

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def __str__(self):
        return self.title
