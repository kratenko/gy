import logging

from pyramid.config import Configurator
from pyramid.events import subscriber, ContextFound, BeforeRender
from pyramid.request import Request
from pyramid import security
from pyramid.decorator import reify
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden
from pyramid_mailer import mailer_factory_from_settings
from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

from sqlalchemy import engine_from_config
from sqlalchemy.orm.exc import NoResultFound

from pyramid_beaker import session_factory_from_settings

from auth import GyAuthenticationPolicy
from auth import GyAuthorizationPolicy
from core.models import (
    DBSession,
    Base,
    Site,
    App,
    User,
    )
from blog.models import Blog

log = logging.getLogger(__name__)



@subscriber(ContextFound)
def check_traversed(event):
    """
    Evaluate traversal result and derive information.

    This is called, after traversal has found it's context.
    """
    request = event.request
    context = request.context
    app = None
    site = None
    current = context
    while current is not None:
        if app is None and isinstance(current, App):
            app = current
        if site is None and isinstance(current, Site):
            site = current
        current = current.__parent__
    # put what we found in request:
    request.site = site
    request.app = app
    request.nav = site.menu_entries


class GyRequest(Request):
    """
    Gy's own request class.
    """
    @reify
    def db(self):
        """
        Return the current DB Session.
        """
#        log.info('fetching request.db')
        return DBSession

    @reify
    def user(self):
        """
        Return User object (if any) or None if not logged in.
        """
#        log.info('fetching request.user')
        # get id of logged in user (if any):
        id = security.authenticated_userid(self)
        if id is None:
            return None
        # fetch that user from DB
        try:
            # return user:
            return self.db.query(User).filter_by(id=id).one()
        except NoResultFound:
            # user not found, so destroy session:
            security.forget(self)
            # no user found, so user is None:
            return None


    def has_permission(self, permission, context=None):
        """
        Check permission on this request.
        """
        if context is None:
            context = self.context
#        log.info("check permission stuff: %s, %s" % (permission, context))
        return has_permission(permission, context, self)


    def require_permission(self, permission, context=None):
        if not self.has_permission(permission, context):
            raise HTTPForbidden


    def admin_active(self):
        return self.session['auth']['admin_active']



def get_root(request):
    """
    Root factory for traversal.

    Return the root node of the resource tree.
    """
    # TODO: how do we know which site to fetch?
    site_name = u'root'
#    log.info(u"fetching site '%s'" % site_name)
    site = DBSession.query(Site).filter_by(name=site_name).one()
    # cap location awareness (for traversal):
    site.__parent__ = None
    site.__name__ = u''
    return site


def gy_not_found(request):
    return HTTPNotFound('4o4')

    
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # the database session:
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

#    session_factory = session_factory_from_settings(settings)
    config = Configurator(
        settings=settings,
        root_factory=get_root,
        authentication_policy=GyAuthenticationPolicy(),
        authorization_policy=GyAuthorizationPolicy(),
        session_factory = session_factory_from_settings(settings),
        request_factory = GyRequest,
    )

    config.add_static_view('static', 'static', cache_max_age=3600)
    
#    config.include('pyramid_mailer')

    mailer = Mailer.from_settings(settings)
    config.registry['mailer'] = mailer

    config.include('gy.core')
    config.include('gy.blog')
    config.add_notfound_view(gy_not_found, append_slash=True)


    config.scan()
    return config.make_wsgi_app()
