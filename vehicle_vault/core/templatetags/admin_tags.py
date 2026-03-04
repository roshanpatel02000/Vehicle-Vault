from django import template
from core.models import User

register = template.Library()

@register.simple_tag
def get_pending_admin_count():
    return User.objects.filter(role='Admin', is_approved=False).count()
