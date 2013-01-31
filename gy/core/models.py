import logging
import re

from markdown import markdown

from pyramid.decorator import reify

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import pbkdf2

from ..tools import slugify

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class columns(object):
    """
    Class to collect column types for models.
    """
    id = sa.Integer
    type = sa.String(64)
    content = sa.UnicodeText()
    node_name = sa.Unicode(128)
    site_name = sa.Unicode(255)
    slug = sa.Unicode(255)
    permission = sa.Unicode(16)
    permission_level = sa.SmallInteger
    language = sa.Unicode(16)
    ip = sa.String(8*4+7)
    email = sa.Unicode(255)



class ItemPermission(Base):
    """
    Permission granted on item to auth entity.
    """
    __tablename__ = 'core_item_permission'
    item_id = sa.Column(columns.id, sa.ForeignKey('core_item.id'), primary_key=True,)
    auth_id = sa.Column(columns.id, sa.ForeignKey('core_item.id'), primary_key=True,)
    permission = sa.Column(columns.permission, primary_key=True)
    item = relationship(
        'Item',
        primaryjoin="ItemPermission.item_id==Item.id",
        backref='permissions',
    )
    auth = relationship(
        'AuthEntity',
        primaryjoin="ItemPermission.auth_id==AuthEntity.id",
    )

    def signature(self):
        return "<Permission: <%d> may <%s> on <%d> >" % (self.auth_id, self.permission, self.item_id)



class Item(Base):
    """
    Base class for all entities.

    Everything that "is something" should be a descendent of this 
    class. Every Item is identified globally by it's id. Permissions 
    are granted on items. Resources in the resource tree are typically 
    items.
    """
    log = logging.getLogger(__name__+'.Item')
    __tablename__ = 'core_item'
    id = sa.Column(columns.id, primary_key=True)
    type = sa.Column(columns.type)
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': ':item',
    }
    parent_id = sa.Column(columns.id, sa.ForeignKey('core_item.id'), nullable=True)
    slug = sa.Column(columns.slug, nullable=True, index=True)

    modified = sa.Column(sa.DateTime, onupdate=text('CURRENT_TIMESTAMP'))
    modify_count = sa.Column(sa.Integer, default=0)
    modifier_id = sa.Column(columns.id, sa.ForeignKey('core_user.id', use_alter=True, name='item_modifier_fk'))
#    modifier_id = sa.Column(columns.id, sa.ForeignKey('core_user.id', schema="User"))
    modifier = relationship(
        'User', 
        primaryjoin="User.id==Item.modifier_id",
#        primaryjoin="core_item.c.modifier_id==core_item.c.id",
        uselist=False,
    )

    created = sa.Column(sa.DateTime, default=text('CURRENT_TIMESTAMP'))
    creator_id = sa.Column(
        columns.id, 
        sa.ForeignKey('core_user.id', use_alter=True, name='item_creator_fk'),
    )
    creator = relationship(
        'User', 
        primaryjoin="Item.creator_id==User.id",
        uselist=False,
    )

    title = sa.Column(sa.Unicode(255), index=True)

    comments_active = sa.Column(sa.Boolean, nullable=False, default=False)
    show_comments = sa.Column(sa.Boolean, nullable=False, default=True)

    language = sa.Column(columns.language)

    content = sa.Column(columns.content)

    children = relationship(
        'Item', 
        primaryjoin="Item.id==Item.parent_id",
        backref=backref('parent', remote_side=[id]),
    )


    def __getitem__(self, key):
        """
        Return child in resource tree (for traversal).
        """
        self.log.info("getting child '%s' from '%s'" % (key, self))
        r = DBSession.query(Item).filter(Item.parent==self, Item.slug==key).first()
        self.log.info("found %s" % r)
        if r is None:
            raise KeyError
        else:
            return r


    def signature(self):
        return u"<#%d/%s>" % (self.id, self.__class__.__name__)


    def short(self):
        return self.title


    @reify
    def __name__(self):
        """
        Return name in resource tree (for traversal).
        """
        if self.slug is None:
            return u''
        return self.slug

    @reify
    def __parent__(self):
        """
        Return parent node in resource tree (for traversal).
        """
        return self.parent

    def render_content(self):
        """
        Return content prepared for display.
        """
        return markdown(self.content)

    def get_permission_object(self):
        """
        Return object used for authorization.
        """
        return self

    def get_permission_id(self):
        """
        Return id used for authorization.
        """
        return self.id

    def get_permissions(self):
        return self.get_permission_object().permissions


    def get_item_menu(self, request, function, parameters):
        return []


    def set_item_tags_by_string(self, tag_string):
        tag_names = [re.sub(r'\W+', u'', _) for _ in re.split(r'[\s,;\.]+', tag_string)]
        for name in tag_names:
            c = DBSession.query(Tag).filter_by(name=name).count()
            if not c:
                tag = Tag(name=name)
                DBSession.add(tag)
        tags = DBSession.query(Tag).filter(Tag.name.in_(tag_names)).all()
        self.tags = tags


    def get_item_tags_string(self):
        return u' '.join([_.name for _ in self.tags])


    def set_item_categories_by_string(self, cat_string):
        cat_names = [re.sub(r'\W+', u'', _) for _ in re.split(r'[\s,;\.]+', cat_string)]
        for name in cat_names:
            c = DBSession.query(Category).filter_by(name=name).count()
            if not c:
                cat = Category(name=name)
                DBSession.add(cat)
        cats = DBSession.query(Category).filter(Category.name.in_(cat_names)).all()
        self.categories = cats


    def get_item_categories_string(self):
        return u' '.join([_.name for _ in self.categories])


    def get_recent_comments(self, count=5):
        return DBSession.query(Comment).filter_by(direct_item=self).order_by('created').all()
        return DBSession.query(Comment).filter_by(direct_item=self).order_by('created').slice(0, count).all()



class AuthEntity(Item):
    """
    Abstract authorization base class.

    Instances of this class (and it's decendents, of course) can 
    be granted permissions on items.
    """
    __mapper_args__ = {
        'polymorphic_identity': ':auth_entity',
    }



class User(AuthEntity):
    """
    Class for users of the application/site.

    Anyone how can log in need's an instance of this. This class 
    is used for managing ownership of and permissions on items of 
    any kind.
    """
    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __tablename__ = 'core_user'
    __mapper_args__ = {
        'polymorphic_identity': ':user',
        'inherit_condition': (Item.id == id),
    }
    name = sa.Column(sa.Unicode(255), unique=True, index=True,)
    is_admin = sa.Column(sa.Boolean(), nullable=False, default=False,)
    full_name = sa.Column(sa.Unicode(255))
    email = sa.Column(columns.email)
    password = sa.Column(sa.Unicode(255))

    def __init__(self, *args, **kwargs):
        AuthEntity.__init__(self, *args, **kwargs)
        self.unset_password()

    def signature(self):
        return u"<#%d/%s:%s>" % (self.id, self.__class__.__name__, self.name)

    def short(self):
        return self.full_name

    def unset_password(self):
        """
        Set password to something unsolveable.
        """
        self.password = '*'

    def set_password(self, password):
        """
        Set password hash to given password.
        """
        self.password = pbkdf2.crypt(password)

    def check_password(self, password):
        """
        Check if password is set to $password.
        """
        return self.password == pbkdf2.crypt(password, self.password)



group_member_table = sa.Table(
    'core_group_member',
    Base.metadata,
    sa.Column(
        'user_id',
        columns.id,
        sa.ForeignKey('core_user.id'),
        primary_key=True,
    ),
    sa.Column(
        'group_id',
        columns.id,
        sa.ForeignKey('core_group.id'),
        primary_key=True,
    ),
)

class Group(AuthEntity):
    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __tablename__ = 'core_group'
    __mapper_args__ = {
        'polymorphic_identity': ':group',
        'inherit_condition': (Item.id == id),
    }
    name = sa.Column(sa.Unicode(255), unique=True,)
    full_name = sa.Column(sa.Unicode(255), )
    description = sa.Column(sa.Unicode(255), )

    members = relationship(
        User,
        secondary=group_member_table,
        backref='groups',
    )

    def signature(self):
        return u"<#%d/%s:%s>" % (self.id, self.__class__.__name__, self.name)

    def short(self):
        return self.full_name




class App(Item):
    """
    Abstract class for applications within a site.

    Applications (e.g. a blog or forum) should inherit from 
    this class. An intance of those applications can than be 
    put into the resource tree.
    """
    __mapper_args__ = {
        'polymorphic_identity': ':app',
    }
    


class Page(Item):
#    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': ':page',
    }

    def __init__(self, title, content=u'', slug=None, parent=None):
        self.title = title
        if slug is None:
            self.slug = slugify(title)
        else:
            self.slug = slug
        self.content = content
        self.parent = parent
    

class Menu(Item):
    id = sa.Column(
        columns.id,
        sa.ForeignKey(Item.id),
        primary_key=True,
        doc="",
    )
    __tablename__ = 'core_menu'
    __mapper_args__ = {
        'polymorphic_identity': ':menu',
    }


class VirtualMenu(object):
    def __init__(self, title=u'Virtual menu', menu_entries=[]):
        self.title = title
        self.menu_entries = menu_entries


class VirtualMenuEntry(object):
    menu_id = None
    number = 0
    target_id = None
    target_path = None
    link_text = None
    link_title = None
    menu = None
    target = None
    target_view = None

    def get_target(self, request):
        return self.target

    def get_url(self, request):
        if self.target_view is None:
            return request.resource_url(self.get_target(request))
        else:
            return request.resource_url(self.get_target(request), self.target_view)


class MenuEntry(Base):
    __tablename__ = 'core_menu_entry'
    menu_id = sa.Column(
        columns.id,
        sa.ForeignKey(Menu.id),
        primary_key=True,
    )
    number = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    target_id = sa.Column(
        columns.id,
        sa.ForeignKey(Item.id),
        nullable=True,
    )
    target_view = sa.Column(
        sa.Unicode(255),
        nullable=True,
    )
    target_path = sa.Column(
        sa.Unicode(255),
        nullable=True,
    )
    link_text = sa.Column(
        sa.Unicode(255),
    )
    link_title = sa.Column(
        sa.Unicode(255),
    )
    menu_function = sa.Column(
        sa.Unicode(255),
    )
    menu_parameters = sa.Column(
        sa.Unicode(255),
    )

    menu = relationship(
        Menu,
        primaryjoin=menu_id==Menu.id,
        backref=backref(
            'menu_entries',
            order_by=number,
        ),
    )

    target = relationship(
        Item,
        primaryjoin=target_id==Item.id,
    )

    def signature(self):
        return u"<MenuEntry:%d->%d>" % ()


    def get_function_parameters(self):
        parms = {}
        if self.menu_parameters is not None:
            for s in self.menu_parameters.split(';'):
                if '=' in s:
                    key, value = s.split('=', 1)
                    parms[key] = value
        return parms


    def get_target(self, request):
        if self.menu_function is not None:
            # build pseudo menu from item:
            parms = self.get_function_parameters()
            return self.target.get_item_menu(request, self.menu_function, parms)
        return self.target


    def get_url(self, request):
        if self.target_view is None:
            return request.resource_url(self.get_target(request))
        else:
            return request.resource_url(self.get_target(request), self.target_view)
    


class Site(Menu):
    id = sa.Column(columns.id, sa.ForeignKey(Menu.id), primary_key=True)
    __tablename__ = 'core_site'
    __mapper_args__ = {
        'polymorphic_identity': ':site',
        'inherit_condition': (Menu.id == id),
    }
    name = sa.Column(
        columns.site_name, 
        unique=True, 
        index=True,
    )
    everyone_id = sa.Column(
        columns.id, 
        sa.ForeignKey(AuthEntity.id),
        doc="ID of AuthEntity that _everyone_ has, logged in or not.",
    )
    users_id = sa.Column(
        columns.id, 
        sa.ForeignKey(AuthEntity.id),
        doc="ID of AuthEntity that every logged in user has.",
    )
    everyone = relationship(
        AuthEntity,
        primaryjoin=everyone_id==AuthEntity.id,
    )
    users = relationship(
        AuthEntity,
        primaryjoin=users_id==AuthEntity.id,
    )



class Comment(Item):
    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __tablename__ = 'core_comment'
    __mapper_args__ = {
        'polymorphic_identity': ':comment',
        'inherit_condition': (Item.id == id),
    }
    main_item_id = sa.Column(columns.id, sa.ForeignKey(Item.id))
    direct_item_id = sa.Column(columns.id, sa.ForeignKey(Item.id))
    depth = sa.Column(sa.SmallInteger, nullable=False, default=0)
    poster_name = sa.Column(sa.Unicode(255), nullable=True,)
    poster_email = sa.Column(columns.email, nullable=True,)
    poster_ip = sa.Column(columns.ip, nullable=True,)
    main_item = relationship(
        Item,
        primaryjoin=main_item_id==Item.id,
        backref='item_comments',
    )
    direct_item = relationship(
        Item,
        primaryjoin=direct_item_id==Item.id,
        backref='direct_comments',
    )
    
    def signature(self):
        return u"<#%d/%s on %s:(%d:%d)>" % (
                self.id, 
                self.__class__.__name__,
                self.main_item.signature(),
                self.direct_item_id,
                self.depth,
            )


item_tag_table = sa.Table(
    'core_item_tag',
    Base.metadata,
    sa.Column(
        'item_id',
        columns.id,
        sa.ForeignKey('core_item.id'),
        primary_key=True,
    ),
    sa.Column(
        'tag_id',
        columns.id,
        sa.ForeignKey('core_tag.id'),
        primary_key=True,
    ),
)


class Tag(Item):
    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __tablename__ = 'core_tag'
    __mapper_args__ = {
        'polymorphic_identity': ':tag',
    }

    name = sa.Column(sa.Unicode(255), index=True, unique=True, nullable=False)

    items = relationship(
        Item,
        secondary=item_tag_table,
        backref='tags',
    )



item_category_table = sa.Table(
    'core_item_category',
    Base.metadata,
    sa.Column(
        'item_id',
        columns.id,
        sa.ForeignKey('core_item.id'),
        primary_key=True,
    ),
    sa.Column(
        'category_id',
        columns.id,
        sa.ForeignKey('core_category.id'),
        primary_key=True,
    ),
)


class Category(Item):
    id = sa.Column(columns.id, sa.ForeignKey(Item.id), primary_key=True)
    __tablename__ = 'core_category'
    __mapper_args__ = {
        'polymorphic_identity': ':category',
    }
    parent_category_id = sa.Column(columns.id, sa.ForeignKey('core_category.id'), nullable=True)

    name = sa.Column(sa.Unicode(255), index=True, unique=True, nullable=False)

    child_categories = relationship(
        'Category',
        primaryjoin="Category.id==Category.parent_category_id",
        backref=backref('parent_category', remote_side=[id])
    )

    items = relationship(
        Item,
        secondary=item_category_table,
        backref='categories',
    )

