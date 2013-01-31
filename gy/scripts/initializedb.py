# *** encoding: utf-8 ***
import os
import sys
import transaction
import datetime
import logging

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..core.models import (
    DBSession,
    Base,
    Site,
    User,
    App,
    Group,
    Page,
    ItemPermission,
    Menu,
    MenuEntry,
    Tag,
    Category,
    Comment,
    )

from ..blog.models import (
    Blog,
    Post,
)

from ..tools import slugify

log = logging.getLogger(__name__)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def gen_users(session):
    """
    Add some garbage users.
    """
    names = (
        ('pete', 'Pete Thornton'),
        ('jack', 'Jack Dalton'),
        ('mac', 'Angus MacGyver'),
        ('harry', 'Harry Jackson'),
        ('magnum', 'Thomas Sullivan Magnum'),
        ('higgins', 'Jonathan Quayle Higgins III'),
        ('tc', 'Theodore Calvin'),
        ('hannibal', 'Colonel Hannibal Smith'),
        ('face', 'Lieutenant First Class Templeton Peck'),
        ('murdock', 'Captain H. M. Murdock'),
        ('ba', 'Master Sergean Bosco Albert Baracus'),
        ('alf', 'Gordon Shumway'),
        ('willie', 'Willie Francis Tanner'),
        ('kate', 'Kate Tanner'),
        ('lynn', 'Lynn Tanner'),
        ('brian', 'Brian Tanner'),
        ('eric', 'Eric Tanner'),
        ('neal', 'Neal Tanner'),
        ('trevor', 'Trevor Ochmonek'),
        ('raquel', 'Raquel Ochmonek'),
        ('jake', 'Jake Ochmonek'),
        ('quincy', 'Dr. R. Quincy'),
        ('sam', 'Sam Fujiyama'),
        ('asten', 'Dr. Robert Asten'),
        ('charles', 'Charles Phillip Ingalls'),
        ('caronline', 'Caroline Lake Quiner Ingalls'),
        ('mary', 'Mary Amelia Ingalls Kendall'),
        ('laura', 'Laura Elizabeth Ingalls Wilder'),
        ('carrie', 'Caroline Celestia Ingalls'),
        ('isaiah', 'Isaiah Edwards'),
        ('harriet', 'Harriet Oleson'),
        ('nellie', 'Nellie Oleson'),
        ('nels', 'Nels Oleson'),
    )
    for p in names:
        user = User(name=p[0], full_name=p[1])
        session.add(user)


def gen_posts(session, blog, user):
    """
    Add some garbage posts to a blog.
    """
    posts = (
        (12.123, u"Emotivismus", u"""Dies ist eines der Wörter, deren Bedeutung mir nicht geläufig ist."""),
        (15.28, u"Gnadenlose Jagt", u"""Er war ein Cop. Ein verdammt guter; aber er machte einen Fehler: er sagte gegen Polizisten aus, die die Fronten gewechselt hatten. Die wollten ihn töten, aber erwischten die Frau die er liebte.\n\nSeit dem durchstreift er das Land. Ein Gesetzloser, der andere Gesetzlose jagt. Ein Kopfgeldjäger. Ein Abtrünniger."""),
        (2.73, u"Controlling table inheritance with mixins", u"""
The `__tablename__` attribute in conjunction with the hierarchy of classes involved in a declarative mixin scenario controls what type of table inheritance, if any, is configured by the declarative extension.

If the `__tablename__` is computed by a mixin, you may need to control which classes get the computed attribute in order to get the type of table inheritance you require.

For example, if you had a mixin that computes `__tablename__` but where you wanted to use that mixin in a single table inheritance hierarchy, you can explicitly specify `__tablename__` as `None` to indicate that the class should not have a table mapped:

    from sqlalchemy.ext.declarative import declared_attr
    
    class Tablename:
        @declared_attr
        def __tablename__(cls):
            return cls.__name__.lower()

    class Person(Tablename, Base):
        id = Column(Integer, primary_key=True)
        discriminator = Column('type', String(50))
        __mapper_args__ = {'polymorphic_on': discriminator}

    class Engineer(Person):
        __tablename__ = None
        __mapper_args__ = {'polymorphic_identity': 'engineer'}
        primary_language = Column(String(50))

    
"""),
        (7.4, u'Soviet', u'When I was in Russia I got into a fight. I was knocked unconcious by ...'),
        (33.11, u'Dominus vobiscum', u'O Lord, we really would need your help right now, but you seem to be occupied elsewhere...'),
        (30.05, u'What the Hex?', u'0xf00f'),
    )
    now = datetime.datetime.now()
    for post_def in posts:
        when = now - datetime.timedelta(post_def[0])
        post = Post(
            created=when,
            creator=user,
            date=when.date(),
            published=True,
            title=post_def[1],
            slug=slugify(post_def[1]),
            content=post_def[2],
            blog=blog,
        )



def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        now = datetime.datetime.now()

        site = Site(name=u'root', title=u'TheSite')
        site.content = u"This is the only content of the main page. Change it!"
        DBSession.add(site)
        site.everyone = Group(name=u'everyone')
        site.users = Group(name=u'users')
        curators = Group(name=u'curators')
        ItemPermission(item=site, auth=site.everyone, permission=u'view')
        ItemPermission(item=site, auth=curators, permission=u'edit')

        admin = User(name=u'admin', full_name=u'The true admin')
        admin.is_admin = True
        admin.email = u'admin@example.org'
        admin.set_password(u'admin')
        curators.members.append(admin)

#        user = User(name=u'user', full_name=u'Just A. User')
#        user.email = u'user@example.org'
#        user.set_password(u'user')
#        DBSession.add(user)

        about = Page(title=u'About TheSite', slug=u'about', parent=site)
        about.content = u"Some cool information about TheSite."
        about.creator = admin
        ItemPermission(item=about, auth=site.everyone, permission=u'view')
        ItemPermission(item=about, auth=curators, permission=u'edit')

        imprint = Page(title=u'Imprint', slug=u'imprint', parent=site)
        imprint.content = u'This site is so new and small. Do we need an imprint?'
        imprint.creator = admin
        ItemPermission(item=imprint, auth=site.everyone, permission=u'view')
        ItemPermission(item=imprint, auth=curators, permission=u'edit')

        blog = Blog(title=u'The Blog', slug=u'blog', parent=site)
        blog.creator = admin
        ItemPermission(item=blog, auth=site.everyone, permission=u'view')
        ItemPermission(item=blog, auth=curators, permission=u'edit')

        post1 = Post(date=now.date(), created=now, creator=admin, 
            title=u"Let's start posting!", blog=blog, published=True,)
        post1.slug = slugify(post1.title)
        post1.content = u"""
We habe a blog now...

Let's start the *postin'*!
"""
        
        cat_new = Category(name=u'news')
        tag_new = Tag(name=u'news')
        tag_blog = Tag(name=u'blog')
        post1.categories = [cat_new]
        post1.tags = [tag_new, tag_blog]

        c1 = Comment(direct_item=post1, main_item=post1, depth=1)
        c1.title = u'Is that so?'
        c1.content = u'I can not really believe that.'
        c1.poster_name=u'Noone'

        menu = Menu(title=u'Navigation')
        MenuEntry(menu=site, number=1, target=menu)
        MenuEntry(menu=site, number=2, target=blog, menu_function='control')
        MenuEntry(menu=site, number=3, target=blog, menu_function='recent_posts')
        MenuEntry(menu=site, number=4, target=blog, menu_function='recent_months')


        MenuEntry(menu=menu, number=1, target=site, link_text=u'Home', link_title=u'To the main page')
        MenuEntry(menu=menu, number=2, target=about, link_text=u'About', link_title=about.title)
        MenuEntry(menu=menu, number=3, target=imprint, link_text=u'Imprint')
        #MenuEntry(menu=menu, number=4, target=imprint, link_text=u'Imprint')
        #MenuEntry(menu=menu, number=5, target=imprint, link_text=u'Imprint')

