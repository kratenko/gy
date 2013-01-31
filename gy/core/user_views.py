from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound


from ..tools import Paginator
from .models import (
    DBSession,
    User,
)


@view_config(
    route_name="core:user.list",
    renderer="gy:templates/core/user/list.html.mako",
)
def list_user(request):
    query = DBSession.query(User).order_by(User.created, User.id)
    paginator = Paginator(request, query=query)
    return {
        'paginator':paginator,
    }
    return Response("Users")


@view_config(
    route_name="core:user",
    renderer="gy:templates/core/user/user.html.mako",
)
def user(request):
    name = request.matchdict['name']
    user = request.db.query(User).filter_by(name=name).one()
    return {
        'name':name,
        'user':user,
    }
