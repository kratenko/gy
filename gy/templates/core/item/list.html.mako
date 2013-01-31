<%inherit file="/base.mako" />
<article>
<table class="list">
  <caption>Users ${paginator.items_from} to ${paginator.items_to} of ${paginator.items_total}</caption>
  <thead>
    <tr>
      <th>id</th>
      <th>type</th>
      <th>slug</th>
      <th>title</th>
    </tr>
  </thead>
  <tfoot>
	<tr>
		<td></td>
		<td colspan="3">
%for page in paginator.page_objects():
  %if page.is_current:
	${page.text}
  %else:
	<a href="${page.url}">${page.text}</a>
  %endif
%endfor
		</td>
	</tr>
  </tfoot>
  <tbody>
% for number, item in paginator.numbered_items():
    <tr>
      <td><a href="${request.route_url('core:item', id=item.id)}">${item.id}</a></td>
      <td>${item.type}</td>
      <td>${item.signature()}</td>
      <td>${item.short()}</td>
##      <td>${item.title}</td>
    </tr>
% endfor
  </tbody>
</table>
</article>
