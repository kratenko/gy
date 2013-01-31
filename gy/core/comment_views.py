import logging
import re

from markdown import markdown

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import sqlalchemy as sa

from gy.core.models import (
    DBSession,
    Item,
    Comment,
)


@view_config(
    context=Item,
    name='comments',
    permission='view'
)
def comments_view(request):
    item = request.context
    return Response("no")
