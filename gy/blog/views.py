import logging
import datetime
from markdown import markdown

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import sqlalchemy as sa

from .models import Blog, Post, Year, Month, Day
from gy.core.models import (
    DBSession,
    Tag,
    Category,
    Comment,
)
from gy.tools import slugify, Paginator



@view_config(
    context=Blog, 
    name="post", 
    renderer="gy:templates/blog/compose.html.mako",
    permission='edit',
)
def post_form(request):
    """View: Form for posting a new post in blog.
    """
    blog = request.context
    title = u''
    slug = u''
    content = u''
    date = datetime.date.today()
    published = False
    tags = u''
    cats = u''
    if request.POST:
        # got post data, let's try to save:
        post = Post(blog=blog)
        post.date = request.POST.get('date', datetime.date.today())
        post.title = request.POST.getone('title')
        post.slug = slugify(request.POST.getone('slug'))
        post.content = request.POST.getone('content')
        post.creator = request.user
        post.set_item_tags_by_string(request.POST.getone('tags'))
        post.set_item_categories_by_string(request.POST.getone('cats'))
        if post.slug == u'':
            post.slug = slugify(post.title)
        post.published = (request.POST.get('published', 'not') == u'published')
        DBSession.flush()
#        return Response('a')
        raise HTTPFound(request.resource_url(blog))

    return {
        'Title':u'Create new post',
        'blog':blog,
        'title':title,
        'slug':slug,
        'content':content,
        'date':date,
        'tags':tags,
        'cats':cats,
        'published_checked':u'checked' if published else u'',
    }



@view_config(
    context=Post, 
    name="delete",
    permission="edit",
    renderer="gy:templates/blog/post.delete.html.mako",
)
def post_delete(request):
    """
    View: Delete a post from blog.
    """
    post = request.context
    blog = post.blog
    if request.POST and request.POST.has_key('.delete'):
        DBSession.delete(post)
        DBSession.flush()
        raise HTTPFound(request.resource_url(blog))

    return {
        'Title':u'Delete post: %s' % post.title,
        'post':post,
        'blog':blog,
    }


@view_config(
    context=Post, 
    name="edit", 
    renderer="gy:templates/blog/post.edit.html.mako",
    permission='edit',
)
def post_edit(request):
    """
    View: Form for editing of blog post.
    """
    post = request.context
    blog = post.blog
    if request.POST:
        # got post data, let's try to save:
        post.date = request.POST.getone('date')
        post.title = request.POST.getone('title')
        post.slug = slugify(request.POST.getone('slug'))
        post.content = request.POST.getone('content')
        if post.slug == u'':
            post.slug = slugify(post.title)
        post.published = (request.POST.get('published', 'not') == u'published')
        post.set_item_tags_by_string(request.POST.getone('tags'))
        post.set_item_categories_by_string(request.POST.getone('cats'))
        DBSession.flush()
        raise HTTPFound(request.resource_url(post))
    
    return {
        'Title':u'Edit post: %s' % post.title,
        'blog':blog,
        'post':post,
        'published_checked':u'checked' if post.published else u'',
    }


@view_config(
    context=Post, 
    name="save",
    permission='edit',
)
def post_save(request):
    """
    View: Save post after edit.
    """
    post = request.context
    post.date = request.POST.getone('date')
    post.title = request.POST.getone('title')
    post.slug = slugify(request.POST.getone('slug'))
    post.content = request.POST.getone('content')
    request.db.flush()
    return HTTPFound(request.resource_url(post))


@view_config(
    context=Post, 
    name="comment", 
    renderer="gy:templates/blog/comment.html.mako",
    permission='view',
)
def post_comment(request):

    return {}


@view_config(
    context=Blog, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
)
@view_config(
    context=Blog, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
    name='tag',
)
@view_config(
    context=Blog, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
    name='category',
)
@view_config(
    context=Year, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
)
@view_config(
    context=Month, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
)
@view_config(
    context=Day, 
    renderer="gy:templates/blog/main.html.mako",
    permission='view',
)
def view_month(request):
    context = request.context
    blog = None
    year = None
    month = None
    day = None
    Title = None
    if isinstance(context, Year):
        year = context
        blog = year.blog
        Title = u'%s, %04d' % (blog.title, year.number)
    elif isinstance(context, Month):
        month = context
        year = month.year
        blog = year.blog
        Title = u'%s, %04d-%02d' % (blog.title, year.number, month.number)
    elif isinstance(context, Day):
        day = context
        month = context
        year = month.year
        blog = year.blog
        Title = u'%s, %04d-%02d-%02d' % (blog.title, year.number, month.number, day.number)
    elif isinstance(context, Blog):
        blog = context
        Title = blog.title
    else:
        Title = blog.title

        
    # build the query
    query = DBSession.query(
        Post
    ).filter_by(
        blog=blog
    )
    if not request.has_permission('edit'):
        query = query.filter(Post.published==True)
    if year:
        query = query.filter(sa.func.year(Post.date)==year.number)
    if month:
        query = query.filter(sa.func.month(Post.date)==month.number)
    if day:
        query = query.filter(sa.func.day(Post.date)==day.number)
    if request.view_name == u'category':
        category_name = request.subpath[0]
        category = DBSession.query(Category).filter_by(name=category_name).first()
        query = query.filter(Post.categories.contains(category))
    if request.view_name == u'tag':
        tag_name = request.subpath[0]
        tag = DBSession.query(Tag).filter_by(name=tag_name).first()
        query = query.filter(Post.tags.contains(tag))
    query = query.order_by('date desc, created desc')
    paginator = Paginator(request, query=query, items_per_page=5)
    return {
        'Title':Title,
        'blog':blog,
        'paginator':paginator,
    }



@view_config(
    context=Post, 
    renderer="gy:templates/blog/post.html.mako",
    permission='view',
)
def view_post(request):
    post = request.context
    blog = post.blog
    if request.POST:
        if request.POST.get('.post_comment'):
            title = request.POST.getone('title')
            content = request.POST.getone('content')
            comment = Comment(main_item=post, direct_item=post)
            comment.title = title
            comment.content = content
            comment.poster_ip = request.remote_addr
            comment.depth = 1
            if request.user is None:
                comment.poster_name = request.POST.getone('name')
                comment.poster_email = request.POST.getone('email')
            else:
                comment.creator = request.user
                comment.owner = request.user

            DBSession.add(comment)
            DBSession.flush()
            raise HTTPFound(request.resource_path(post))
    return {
        'blog':blog,
        'post':post,
    }

