<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  %if Title:
    <title>${request.site.title} &ndash; ${Title}</title> 
  %else:
    <title>${request.site.title}</title>
  %endif
  <!-- [if tl IE 9]>
    <script src="http://html5shov.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
  <link rel="stylesheet" media="all" href="/static/style/gy.css">
  <!-- twitter -->
</head>
<body>
  <header>
    <a href="/" id="gy:main_logo"><img src="/static/img/logo.png" width="400" height="171" alt="Logo" id="gy:main_logo"></a>
  </header>

  <div id="gy:main_body">
    ${next.body()}
  </div>

  <footer>
%  if False and request.context and hasattr(request.context, 'children'):
    <p>
      child nodes of ${request.context.title}
      <ul>
%      for child in request.context.children:
        <li><a href="${request.resource_url(child)}">${child.slug}</a>: ${child.title}</li>
%      endfor
      </ul>
    </p>
%  endif
  </footer>

  <div id="gy:personal">
    <ul>
%    if request.user is None:
      <li><a href="${request.route_url('core:login')}">Log in</a></li>
      <li><a href="${request.route_url('core:login.register')}">Register</a></li>
%    else:
      <li><a href="${request.route_url('core:profile')}">${request.user.full_name}</a></li>
%      if request.user.is_admin:
%        if request.admin_active():
          <li><a href="${request.route_url('core:admin')}">admin</a></li>
	  <li><a href="${request.route_url('core:admin.deactivate')}">deactivate admin</a></li>
%        else:
          <li><a href="${request.route_url('core:admin.activate')}">activate admin</a></li>
%        endif
%      endif
      <li><a href="${request.route_url('core:login.out')}">Log out</a></li>
%    endif
    </ul>
  </div>

  <nav id="gy:menu">
    %for entry in request.nav:
    	<%include file="menu.html.mako" args="menu=entry.get_target(request)" />
    %endfor
  </nav>
</body>
</html>
