import unidecode
import re
import math
import random
import string

def slugify(s):
    # unicode? we just want ascii
    s = unidecode.unidecode(s)
    # remove ' from string (don't want then to turn into -, 
    # like "don't" to "don-t")
    s = re.sub(r"'+", '', s)
    # change non word chars to -
    s = re.sub(r'\W+', '-', s)
    # lower case string
    s = s.lower()
    # remove leading and trailing -
    s = re.sub(r'^-+', '', s)
    s = re.sub(r'-+$', '', s)
    return s


def random_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in xrange(length))


def password_valid(password):
    minlen = 5
    if re.match(r'\s', password):
        return False, "Password my not contain whitespaces (blank, tab, etc.)."
    if len(password) < minlen:
        return False, "Password must be at least %d characters long." % minlen
    return True, None


class Paginator(object):
    class Page(object):
        def __init__(self, number, url, text, is_current=False):
            self.number = number
            self.url = url
            self.is_current = is_current
            self.text = text


    def __init__(self, request, query, prefix=None, items_per_page=10):
        self.request = request
        self.query = query
        self.prefix = prefix
        self.items_per_page = items_per_page

        self.page_number = int(self.request.GET.get(self.parm_name('page'), 1))
        self.items_total = self.query.count()
        self.items_from = self.items_per_page * (self.page_number - 1) + 1
        if self.items_from < 0:
            self.items_from = 0
        self.items_to = self.items_from + self.items_per_page - 1
        if self.items_to > self.items_total:
            self.items_to = self.items_total
        self.items = self.query.slice(self.items_from - 1, self.items_to).all()
        self.pages_total = int(math.ceil(1.0 * self.items_total/self.items_per_page))
        self.pages = range(1, self.pages_total + 1)
        self.prev_page = max(self.page_number - 1, 1)
        self.next_page = min(self.page_number + 1, self.pages_total)
    

    def numbered_items(self):
        for num, item in enumerate(self.items):
            yield num + self.items_from, item


    def _gen_url(self, parms):
        if parms.get('page', '2') == '1':
            del parms['page']
        try:
            return self.request.current_route_path(_query=parms)
        except ValueError:
            return self.request.resource_path(self.request.context, query=parms)
    

    def page_objects(self):
        page_parm = self.parm_name('page')
        # copy given parms
        parms = self.request.GET
        # "go back" link
        parms[page_parm] = str(self.prev_page)
        yield self.Page(
            number=None, 
            url=self._gen_url(parms),
            text="<<",
        )
        for page in self.pages:
            # overwrite page number parameter
            parms[page_parm] = str(page)
            # yield
            yield self.Page(
                number=page, 
                url=self._gen_url(parms),
                text=str(page),
                is_current=(page==self.page_number),
            )
        # "go next" link
        parms[page_parm] = str(self.next_page)
        yield self.Page(
            number=None, 
            url=self._gen_url(parms),
            text=">>",
        )


    def parm_name(self, name):
        if self.prefix is None:
            return name
        else:
            return "%s_%s" % (self.prefix, name)


