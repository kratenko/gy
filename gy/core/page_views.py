import logging

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Item,
    Site,
    Page,
    ItemPermission,
    AuthEntity,
    )
from markdown import markdown

from gy.tools import slugify

log = logging.getLogger(__name__)


#@view_config(context=Site, renderer="gy:templates/site.view.mako")
#def siteviewer(request):
#    site = request.context
#    user = request.user
#
#    return {
#        'site':site,
#    }


@view_config(
    context=Site, 
    renderer="gy:templates/core/page/view.html.mako",
    permission='view',
)
@view_config(
    context=Page, 
    renderer="gy:templates/core/page/view.html.mako",
    permission='view',
)
def pageview(request):
    page = request.context
    return {
        'Title':page.title,
        'page':page,
        'rendered':markdown(page.content, output_format="html5"),
    }


@view_config(
    context=Site, 
    name="edit", 
    renderer="gy:templates/core/page/edit.html.mako",
    permission='edit',
)
@view_config(
    context=Page, 
    name="edit", 
    renderer="gy:templates/core/page/edit.html.mako",
    permission="edit",
)
def pageedit(request):
    page = request.context
    if request.POST:
        page.title = request.POST.getone('title')
        page.slug = request.POST.getone('slug')
        page.content = request.POST.getone('content')
        return HTTPFound(request.resource_url(page))
    return {
        'Title':'Edit page: %s' % page.title,
        'page':page,
    }


@view_config(
    context=Page,
    name="new",
    renderer="gy:templates/core/page/new.html.mako",
)
@view_config(
    context=Site,
    name="new",
    renderer="gy:templates/core/page/new.html.mako",
)
def newpage(request):
    parent = request.context
    title = u''
    slug = u''
    content = u''
    if request.POST:
        slug = slugify(request.POST.getone('slug'))
        if slug == u'':
            slug = None
        page = Page(
            title=request.POST.getone('title'),
            content=request.POST.getone('content'),
            parent=parent,
            slug=slug,
        )
        page.creator = request.user
        if page.slug == u'':
            page.slug = 'xxx'
        slug = page.slug
        DBSession.add(page)
        # copy permissions from parent
        parent_perms = DBSession.query(ItemPermission).filter_by(item=parent).all()
        for parent_perm in parent_perms:
            perm = ItemPermission(item=page, auth=parent_perm.auth, permission=parent_perm.permission)
            DBSession.add(perm)
        DBSession.flush()
        page = DBSession.query(Page).filter_by(parent=parent, slug=slug).one()
        raise HTTPFound(request.resource_url(page))
    return {
        'Title':'Create new page',
        'parent_page':parent,
        'title':title,
        'slug':slug,
        'content':content,
    }


@view_config(
    context=Page,
    name='manage',
    permission='manage',
    renderer='gy:templates/core/page/manage.html.mako',
)
def manage_page(request):
    page = request.context
    if request.POST:
        if request.POST.get('.add_permission'):
            auth_id = long(request.POST.getone('auth'))
            permission = request.POST.getone('permission')
            auth = DBSession.query(AuthEntity).filter_by(id=auth_id).one()
            perm = ItemPermission(item=page, auth=auth, permission=permission)
            DBSession.add(perm)
            DBSession.flush()
            raise HTTPFound(request.resource_path(page, 'manage'))
        elif request.POST.get('.remove_permission'):
            for s in request.POST.getall('permission'):
                auth_id, permission = s.split('.', 1)
                perm = DBSession.query(ItemPermission).filter_by(item=page, auth_id=long(auth_id), permission=permission).first()
                if perm:
                    DBSession.delete(perm)
            DBSession.flush()
            raise HTTPFound(request.resource_path(page, 'manage'))
        elif request.POST.get('.delete_page'):
            parent = page.parent
            for perm in page.permissions:
                DBSession.delete(perm)
            DBSession.delete(page)
            DBSession.flush()
            raise HTTPFound(request.resource_path(parent))
        elif request.POST.get('.move_page'):
            new_parent_id = long(request.POST.getone('new_parent'))
            new_parent = DBSession.query(Item).filter_by(id=new_parent_id).one()
            page.parent = new_parent
            DBSession.flush()
            raise HTTPFound(request.resource_path(page))

    return {
        'Title':'Manage page: %s' % page.title,
        'page':page,
    }

