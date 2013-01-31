<%page args="menu" />
<div class="portlet">
%if menu.title:
  <h5>${menu.title}</h5>
%endif
<ul>
%for entry in menu.menu_entries:
  <li>
    %if entry.link_title is None:
      <a href="${entry.get_url(request)}">${entry.link_text}</a>
    %else:
      <a href="${entry.get_url(request)}" title="${entry.link_title}">${entry.link_text}</a>
    %endif
  </li>
%endfor
</ul>
</div>
