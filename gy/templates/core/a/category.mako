<%page args="category, app=None" />
%if app:
  <a class="gy:category" href="${request.resource_path(app, 'category', category.name)}">${category.name}</a>
%else:
  <a class="gy:category" href="${request.resource_path(category)}">${category.name}</a>
%endif
