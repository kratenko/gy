<%inherit file="/base.mako" />
<article class="gy:page">
  <header>
    <h1 class="title">${Title}</h1>
    %if request.has_permission('edit'):
      <span class="gy:edit_item">
        <a class="gy:edit_link" href="${request.resource_url(page, 'new')}" title="create new page under this one">new</a>
	%if page.type <> ':site':
          <a class="gy:edit_link" href="${request.resource_url(page, 'manage')}">manage</a>
	%endif
        <a class="gy:edit_link" href="${request.resource_url(page, 'edit')}">edit</a>
      </span>
    %endif
  </header>
  ${rendered|n}
</article>
