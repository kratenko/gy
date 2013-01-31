from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


from ..tools import Paginator
from .models import (
    DBSession,
    User,
    Item,
)



@view_config(
    route_name="core:item.list",
    renderer="gy:templates/core/item/list.html.mako",
)
def list_user(request):
    query = DBSession.query(Item).order_by(Item.id)
    paginator = Paginator(request, query=query)
    return {
        'paginator':paginator,
    }


@view_config(
    route_name="core:item",
    renderer="gy:templates/core/item/item.html.mako",
)
def user(request):
    id = long(request.matchdict['id'])
    item = request.db.query(Item).filter_by(id=id).one()
    #perm_ob = item.get_permission_object()
    permissions = item.get_permissions()

    return {
        'id':id,
        'item':item,
        'permissions':permissions,
    }
