<%page args="tag, app=None" />
%if app:
  <a class="gy:tag" href="${request.resource_path(app, 'tag', tag.name)}">${tag.name}</a>
%else:
  <a class="gy:tag" href="${request.resource_path(tag)}">${tag.name}</a>
%endif
