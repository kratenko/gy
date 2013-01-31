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

from sqlalchemy.orm.exc import NoResultFound

from gy.tools import random_password
from ..core.models import (
    DBSession,
    User,
)

log = logging.getLogger(__name__)



@view_config(
    route_name="core:login", 
    renderer="gy:templates/core/login/form.html.mako",
)
def view_login(request):
    """
    View for login form and logging in.
    """
    failed = False
    reason = None
    if request.POST:
        # login request submitted:
        name = request.POST.getone('name')
        password = request.POST.getone('password')
        try:
            user = DBSession.query(User).filter_by(name=name).one()
        except NoResultFound:
            failed = True
            reason = u'That password is not correct for that user.'
        else:
            if user.check_password(password):
                # password correct, log in user for this session:
                security.remember(request, user)
                raise HTTPFound('/')
            else:
                failed = True
                reason = u'That password is not correct for that user.'
    return {
        'Title': 'Login',
        'failed': failed,
        'reason': reason,
    }




@view_config(
    route_name="core:login.out", 
)
def login_out(request):
    """
    View for logging out.
    """
    security.forget(request)
    return HTTPFound('/')


#
from formencode import Schema, validators
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

class UserRegistrationSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True
    name = validators.MinLength(5, not_empty=True)
    full_name = validators.MinLength(5, not_empty=True)

#    form = Form(request, schema=UserRegistrationSchema, )
#    if form.

@view_config(
    route_name='core:login.register',
    renderer="gy:templates/core/login/register.html.mako",
)
def login_register(request):
    c = {
        'name':u'',
        'name.hint':u'',
        'full_name':u'',
        'full_name.hint':u'',
        'email':u'',
        'email.hint':u'',
    }
    if request.POST:
        # submitted:
        name = request.POST.getone('name')
        full_name = request.POST.getone('full_name')
        email = request.POST.getone('email')
        user = User(name=name, full_name=full_name, email=email)
        password = random_password()
        user.set_password(password)
        request.db.add(user)
        body = render(
            'gy:templates/core/login/register_mail.txt.mako',
            {'username':user.name, 'password':password,},
            request=request,
        )
        message = Message(
            subject="User registration on page",
            recipients=[user.email],
            body = body,
        )
        request.registry['mailer'].send(message)
        return HTTPFound(request.route_url('core:login'))
    return {
        'Title':u'Register new user',
    }


@view_config(
    route_name='core:login.reset_password',
    renderer="gy:templates/core/login/reset_password.html.mako",
)
def login_reset_password(request):
    if request.POST:
        name = request.POST.getone('name')
        user = request.db.query(User).filter_by(name=name).one()
        address = user.email
        new_pass = random_password()
        user.set_password(new_pass)
        message = Message(
                    subject=u"Password reset",
                    recipients=[address],
                    body=u"Note quite so. %s" % new_pass,
                )
#        mailer = get_mailer(request)
        request.registry['mailer'].send(message)
    return {
        'Title':u'Reset password',
        'done':False,
        'failed':False,
    }
    
