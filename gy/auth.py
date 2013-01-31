import logging
import time

from zope.interface import implements
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.interfaces import IAuthorizationPolicy

from sqlalchemy import sql

from core.models import DBSession, ItemPermission

log = logging.getLogger(__name__)


class GyAuthenticationPolicy(object):
    implements(IAuthenticationPolicy)

    def _build_auth(self):
#        log.info('building auth')
        pass

    def unauthenticated_userid(self, request):
#        log.info('unauthenticated_userid')
        return None


    def authenticated_userid(self, request):
#        log.info('authenticated_userid')
        try:
            return request.session['auth']['id']
        except KeyError:
            return None


    def effective_principals(self, request):
#        log.info('effective_principals')
        site = request.site
        try:
            principals = request.session['auth']['ep'].union(frozenset([site.everyone_id, site.users_id]))
            if request.session['auth']['admin_active']:
                return principals.union(frozenset([0L]))
            return principals
        except KeyError:
            return [site.everyone_id]


    def remember(self, request, principal, **kw):
#        log.info('remember')
        user = principal
        ep = set([user.id])
        for group in user.groups:
            ep.add(group.id)
        request.session['auth'] = {
            'name':user.name,
            'full_name':user.full_name,
            'id':user.id,
            'ep':frozenset(ep),
            'checked':time.time(),
            'is_admin':user.is_admin,
            'admin_active':False,
        }
        # return empty sequence, since we are not storing information
        # directly in the cookie (using sessions)
        return []


    def forget(self, request):
#        log.info('forget')
        del request.session['auth']
        return []



class GyAuthorizationPolicy(object):
    implements(IAuthorizationPolicy)

    def principals_allowed_by_permission(self, context, permission):
        # We don't do that (at least not yet)
        log.info("principals_allowed_by_permission called")
        return NotImplementedError


    def permits(self, context, principals, permission):
#        log.info("permits %s, %s, %s", context, principals, permission)
        if 0L in principals:
            # admin may do everything:
            return True
        permission_id = context.get_permission_id()
        result = DBSession.query(
            sql.exists(
                [ItemPermission.item_id],
                ItemPermission.auth_id.in_(principals)
            ).where(
                ItemPermission.item_id==permission_id,
            ).where(
                ItemPermission.permission==permission,
            )
        ).scalar()
        return result

