"""blogアプリで主に使用するフィルタ"""
from django.utils import timezone
from django import template
from django.template.defaultfilters import urlize
register = template.Library()

from VMforBeginnerApp.utils import url_replace as ul
from VMforBeginnerApp.utils import url_replace_with_nodelete as ulwn


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータを一部を置き換える"""

    url_dict = request.GET.copy()
    return ul(url_dict, field, value)


@register.simple_tag
def url_replace_with_nodelete(request, field=None, value=None):
    """GETパラメータを一部を置き換える。deleteパスを削除する"""

    url_dict = request.GET.copy()
    return ulwn(url_dict, field, value)

@register.simple_tag
def by_the_time(dt):
    """その時間が今からどのぐらい前か、人にやさしい表現で返す"""

    result = timezone.now() - dt
    s = result.total_seconds()
    hours = int(s / 3600)
    if hours >= 24:
        day = int(hours / 24)
        return '約{0}日前'.format(day)
    elif hours == 0:
        minute = int(s / 60)
        return '約{0}分前'.format(minute)
    else:
        return '約{0}時間前'.format(hours)


@register.filter(is_safe=True)
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" rel="nofollow" ')
