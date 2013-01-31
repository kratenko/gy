<%page args="user" />
% if user is None:
	None
% else:
	<a class="user" href="${request.route_url('core:user', name=user.name)}">${user.name}</a>
% endif:
