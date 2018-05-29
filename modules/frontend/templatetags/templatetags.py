from django import template
from django.contrib.auth.models import User
from django.utils.text import slugify

register = template.Library()


@register.simple_tag
def slug_url(value):
    slug = slugify(value)

    return slug


@register.simple_tag
def check_perms(username, *args, **kwargs):
    get_users = User.objects.get(username=username)
    module = args[0]
    try:
        group = get_users.groups.get()
        module_perms = []
        perms = []
        permission = group.permissions.all()
        for row in permission:

            if kwargs:
                if row.codename not in perms:
                    perms.append(row.codename)
            else:
                if row.content_type.name not in module_perms:
                    module_perms.append(row.content_type.name)

        if kwargs :
            if kwargs['action'] in perms:
                return True
            else:
                return False

        else:
            if module in module_perms:
                return True
            else:
                return False
    except :

        return False

