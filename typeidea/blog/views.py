from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Post, Tag, Category
from config.models import SideBar


# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag, category = None, None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {"post_list": post_list,
               "tag": tag,
               "category": category,
               "sidebars": SideBar.get_all()}
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {"post": post}
    return render(request, 'blog/detail.html', context=context)


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 2

    context_object_name = 'post_list'
    template_name = 'blog/list.html'
