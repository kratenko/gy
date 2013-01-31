<%inherit file="/base.mako" />
<article>
<table class="list">
  <caption>Users ${paginator.items_from} to ${paginator.items_to} of ${paginator.items_total}</caption>
  <thead>
    <tr>
      <th>#</th>
      <th>User</th>
      <th>Name</th>
      <th>joined</th>
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
% for number, user in paginator.numbered_items():
    <tr>
      <td class="number">${number}</td>
      <td><a href="${request.route_url('core:user', name=user.name)}">${user.name}</a></td>
      <td>${user.full_name}</a></td>
      <td>${user.created}</a></td>
    </tr>
% endfor
  </tbody>
</table>
</article>
