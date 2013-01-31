import logging
log = None

def includeme(config):
    global log
    log = logging.getLogger(__name__)
    log.info('including package')
    # adding routes for admin views:
    config.add_route('core:admin', 'admin/')
    config.add_route('core:admin.activate', 'admin/activate')
    config.add_route('core:admin.deactivate', 'admin/deactivate')
    config.add_route('core:admin.menu', 'admin/menu')
    config.add_route('core:admin.menu_entry', 'admin/menu-entry')
    config.add_route('core:admin.delete', 'admin/delete/{id}')
    # adding routes for item manipulation:
    config.add_route('core:item.list', 'item/')
    config.add_route('core:item', 'item/{id}/')
    # adding routes for user information/manipulation:
    config.add_route('core:user.list', 'user/')
    config.add_route('core:user', 'user/{name}/')
    # adding routes for login/etc
    config.add_route('core:login', 'login')
#    config.add_route('core:login.in', 'login/in')
    config.add_route('core:login.out', 'login/out')
    config.add_route('core:login.register', 'login/register')
    config.add_route('core:login.reset_password', 'login/reset-password')
    # addin routes for the user profile/settings
    config.add_route('core:profile', 'profile/')

