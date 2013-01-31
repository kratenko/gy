import logging
import re
import datetime

from markdown import markdown

from pyramid.decorator import reify

import sqlalchemy as sa
from sqlalchemy.orm import (
    relationship,
)
from sqlalchemy.orm.exc import NoResultFound

from ..tools import slugify

import gy.core.models as cm
from ..core.models import DBSession

log = logging.getLogger(__name__)



class Day(object):
    """
    Day context for traversal.

    Item put in traversal tree as context for showing posts 
    of a certain day. Example url:
    http://example.org/blog/2013/01/22/
    """
    def __init__(self, month, key):
        """
        Contructor for blog day context object.
        """
        self.__parent__ = month
        self.__name__ = key
        self.blog = month.blog
        self.month = month
        self.year = month.__parent__
        self.number = int(key)
        self.date = datetime.date(self.year.number, self.month.number, self.number)


    def __getitem__(self, key):
        """
        Get child by name (for traversal).
        """
        log.info("querying post %s, %s:%s" % (self.blog, self.date, key))
        try:
            post = DBSession.query(Post).filter_by(blog=self.blog, date=self.date, slug=key).one()
            # make location aware
            post.__parent__ = self
            return post
        except NoResultFound:
            raise KeyError


    def get_permisson_object(self):
        """
        Return object used for authorization.
        """
        return self.blog


    def get_permission_id(self):
        """
        Return item-id used for authorization.
        """
        return self.blog.id



class Month(object):
    """
    Month context for traversal.

    Item put in traversal tree as context for showing posts 
    of a certain month. Example url:
    http://example.org/blog/2013/01/
    """
    def __init__(self, year, key):
        """
        Contructor for blog month context object.
        """
        self.__parent__ = year
        self.__name__ = key
        self.year = year
        self.blog = year.blog
        self.number = int(key)


    def __getitem__(self, key):
        """
        Return child by name for traversal.
        """
        if re.match(r"^\d\d$", key):
            return Day(self, key)
        raise KeyError


    def get_name(self):
        """
        Return written name of month.
        """
        names = (
            None,
            'January', 'February', 'March',
            'April', 'May', 'June',
            'Juli', 'August', 'September',
            'October', 'November', 'December',
        )
        return names[self.number]


    def get_permisson_object(self):
        """
        Return object used for authorization.
        """
        return self.blog


    def get_permission_id(self):
        """
        Return item-id used for authorization.
        """
        return self.blog.id


    def get_post_count(self):
        return cm.DBSession.query(Post).filter(
            Post.blog==self.blog,
            Post.published==True,
            sa.func.year(Post.date)==self.year.number,
            sa.func.month(Post.date)==self.number,
        ).count()


    def get_unpublished_post_count(self):
        return cm.DBSession.query(Post).filter(
            Post.blog==self.blog,
            Post.published==False,
            sa.func.year(Post.date)==self.year.number,
            sa.func.month(Post.date)==self.number,
        ).count()
        


class Year(object):
    """
    Year context for traversal.

    Item put in traversal tree as context for showing posts 
    of a certain year. Example url:
    http://example.org/blog/2013/
    """
    def __init__(self, blog, key):
        """
        Contructor for blog year context object.
        """
        self.__parent__ = blog
        self.__name__ = key
        self.blog = blog
        self.number = int(key)


    def __getitem__(self, key):
        """
        Return child by name (for traversal).
        """
        if re.match(r"^\d\d$", key):
            return Month(self, key)
        raise KeyError


    def get_permisson_object(self):
        """
        Return object used for authorization.
        """
        return self.blog


    def get_permission_id(self):
        """
        Return item-id used for authorization.
        """
        return self.blog.id



class Blog(cm.App):
    """
    Blog application class.

    Blog objects can be put in resource tree at position where
    blog should be. Multiple independent blogs can be added to 
    any site.
    """

    __mapper_args__ = {
        'polymorphic_identity': 'blog:blog',
    }


    def __getitem__(self, key):
        """
        Return child (for traveral).

        For blogs the direct children will be Year-objects, to 
        implement listing of blog posts per Year/Month/Day.
        """
        if re.match(r"^\d{4}$", key):
            # year
            return Year(self, key)
        raise KeyError


    def get_recent_posts(self, request, count):
        """
        Return last $count posts.
        """
        if request.has_permission('edit'):
            return DBSession.query(Post).filter_by(blog=self).order_by('created desc').slice(0, count).all()
        else:
            return DBSession.query(Post).filter_by(blog=self, published=True).order_by('created desc').slice(0, count).all()


    def get_recent_months(self, request, count):
        """
        Return the last $count months.
        """
        query = DBSession.query(
            sa.func.year(Post.date),
            sa.func.month(Post.date), 
            sa.func.count(Post.date)
        ).filter(
            Post.blog_id==self.id
        ).group_by(
            sa.func.year(Post.date), sa.func.month(Post.date)
        ).order_by(
            sa.desc(sa.func.year(Post.date)), 
            sa.desc(sa.func.month(Post.date))
        )
        ret = []
        for y, m, n in query.all():
            year = Year(self, "%04d" % y)
            month = Month(year, "%02d" % m)
            month.post_count = n
            ret.append(month)
        return ret


    def get_item_menu(self, request, function, parameters):
        if function == 'control':
            blog_entry = cm.VirtualMenuEntry()
            blog_entry.target = self
            blog_entry.link_text = u'Blog'
            blog_entry.link_title = self.title
            post_entry = cm.VirtualMenuEntry()
            post_entry.target = self
            post_entry.link_text = u'New post'
            post_entry.link_title = u'Post a new post'
            post_entry.target_view = 'post'
            if request.has_permission('edit', self):
                ent = [blog_entry, post_entry]
            else:
                ent = [blog_entry]
            menu = cm.VirtualMenu(
                title=u'Blog',
                menu_entries=ent,
            )
            return menu
        elif function == 'recent_posts':
            entries = int(parameters.get('entries', 5))
            posts = self.get_recent_posts(request, entries)
            ent = []
            for n, p in enumerate(posts):
                e = cm.VirtualMenuEntry()
                e.target = p
                e.number = n
                if p.published:
                    e.link_text = p.title
                    e.link_title = u'posted on %s' % p.date
                else:
                    e.link_text = u'(%s)' % p.title
                    e.link_title = u'not posted on %s' % p.date
                ent.append(e)
            menu = cm.VirtualMenu(
                title=parameters.get('title', 'Recent posts'),
                menu_entries=ent,
            )
            return menu
        elif function == 'recent_months':
            entries = int(parameters.get('entries', 5))
            months = self.get_recent_months(request, entries)
            ent = []
            may_edit = request.has_permission('edit', self)
            for n, m in enumerate(months):
                e = cm.VirtualMenuEntry()
                e.target = m
                e.number = n
                post_count = m.get_post_count()
                if may_edit:
                    upost_count = m.get_unpublished_post_count()
                    e.link_text = u"%s %d (%d) (%d)" % (m.get_name(), m.year.number, post_count, upost_count)
                else:
                    e.link_text = u"%s %d (%d)" % (m.get_name(), m.year.number, post_count)
                if post_count == 1:
                    e.link_title = u'1 post in %s %d' % (m.get_name(), m.year.number)
                else:
                    e.link_title = u'%d posts in %s %d' % (post_count, m.get_name(), m.year.number)
                ent.append(e)
            menu = cm.VirtualMenu(
                title=parameters.get('title', 'Older posts'),
                menu_entries=ent,
            )
            return menu
        return cm.VirtualMenu()
        



class Post(cm.Item):
    """
    Blog post class.

    Instances of this class represent individual posts in a
    blog.
    """

    id = sa.Column(
        cm.columns.id, 
        sa.ForeignKey(cm.Item.id), 
        primary_key=True,
        doc="Item-id of this post.",
    )

    blog_id = sa.Column(
        cm.columns.id,
        sa.ForeignKey(Blog.id),
        doc='id of blog this post belongs to',
    )

    __tablename__ = 'blog_post'

    __mapper_args__ = {
        'polymorphic_identity': 'blog:post',
        'inherit_condition': (cm.Item.id == id),
    }


    date = sa.Column(
        sa.Date, 
        index=True,
        doc="""Date of publication. Used in url for post. 
               Should not be changed after publication.""",
    )

    published = sa.Column(
        sa.Boolean, 
        nullable=False, 
        default=False,
        doc="Is post currently published?",
    )

    blog = relationship(
        Blog,
        primaryjoin="Blog.id==Post.blog_id",
        backref='posts'
    )


    def short(self):
        return "%s/%s" % (self.date, self.title)


    @reify
    def __parent__(self):
        """
        Return parent in resource tree (for traversal).

        For blog posts this creates a Year, Month, and Day
        object needed for the url.
        """
        year = Year(self.blog, "%04d" % self.date.year)
        month = Month(year, "%02d" % self.date.month)
        day = Day(month, "%02d" % self.date.day)
        return day


    def get_permission_object(self):
        """
        Return object used for authorization.
        """
        return self.blog


    def get_permission_id(self):
        """
        Return item id used for authorization.
        """
        return self.blog_id


