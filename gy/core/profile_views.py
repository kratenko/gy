import logging
import re
import random
import string

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid import security
from pyramid.renderers import render
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from gy.tools import random_password, password_valid
from ..core.models import (
    DBSession,
    User,
)

log = logging.getLogger(__name__)



@view_config(
    route_name="core:profile", 
    renderer="gy:templates/core/profile/view.html.mako",
)
def profile(request):
    done = False
    failed = False
    if request.POST:
        old = request.POST.getone('old')
        new1 = request.POST.getone('new1')
        new2 = request.POST.getone('new2')
        is_valid, reason_not = password_valid(new1)
        if not is_valid:
            failed = reason_not
        elif new1 != new2:
            failed = 'Two new passwords did not match.'
        elif not request.user.check_password(old):
            failed = 'Your current password was wrong.'
        else:
            request.user.set_password(new1)
            done = True
    return {
        'Title':u'User profile',
        'done':done,
        'failed':failed,
    }


