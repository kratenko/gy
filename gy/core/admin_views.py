import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid import security

from ..core.models import (
    DBSession,
    User,
    Site,
    Menu,
    MenuEntry,
    Item,
    ItemPermission,
)

log = logging.getLogger(__name__)


@view_config(
    route_name="core:admin", 
    renderer="gy:templates/core/admin/admin.html.mako",
    permission='admin',
)
def admin(request):
    """
    View for main admin page.
    """
    return {
        'Title':'Administration area',
    }


@view_config(
    route_name="core:admin.activate", 
    renderer="gy:templates/core/admin/activate.html.mako",
)
def admin_activate(request):
    """
    View for activation of admin functionallity.

    By default when admin users log in, the admin permissions 
    are not activated (to make it possible for admins to do 
    normal work and harder for others to do bad things when an 
    admin is logged in).
    """
    failed = False
    if request.POST:
        password = request.POST.getone('password')
        if request.user.check_password(password):
            request.session['auth']['admin_active'] = True
            raise HTTPFound("/")
        else:
            failed = True
    # print form:
    return {
        'Title':'Activate admin',
        'failed':failed,
    }


@view_config(
    route_name="core:admin.deactivate", 
)
def admin_deactivate(request):
    request.session['auth']['admin_active'] = False
    return HTTPFound('/')



@view_config(
    route_name='core:admin.menu',
    renderer='gy:templates/core/admin/menu.html.mako',
    permission='admin',
)
def admin_menu(request):
    #entries = DBSession.query(MenuEntry).filter_by(menu=request.site).order_by(MenuEntry.number).all()
    return {
        'Title':u'Menus of site %s' % request.site.title,
        'entries':request.site.menu_entries,
    }


@view_config(
    route_name="core:admin.menu_entry",
    renderer='gy:templates/core/admin/entry.html.mako',
    permission='admin',
)
def admin_menu_entry(request):
    menu_id = request.GET.getone('menu')
    number = request.GET.getone('number')
    entry = DBSession.query(MenuEntry).filter_by(menu_id=menu_id, number=number).one()
    return {
        'entry':entry,
        'Title':u'Edit menu entry',
        
    }


@view_config(
    route_name='core:admin.delete',
    renderer='gy:templates/core/admin/delete.html.mako',
    permission='admin',
)
def admin_delete(request):
    item_id = long(request.matchdict['id'])
    item = DBSession.query(Item).filter_by(id=item_id).one()
    if request.POST:
        if request.POST.get('.delete_item'):
            for perm in DBSession.query(ItemPermission).filter_by(item_id=item_id).all():
                DBSession.delete(perm)
            for perm in DBSession.query(ItemPermission).filter_by(auth_id=item_id).all():
                DBSession.delete(perm)
            DBSession.delete(item)
            DBSession.flush()
            raise HTTPFound('')
    return {
        'Title':u'Delete item',
        'item':item,
    }

