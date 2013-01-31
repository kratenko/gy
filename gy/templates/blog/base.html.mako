<%inherit file="/base.mako" />

##<header class="app blog">
##<h1><a href="${request.resource_url(blog)}">Blog: ${blog.title}</a></h1>
##</header>

${next.body()}

<%doc>
<nav class="blog">
	<ul><caption>recent posts</caption>
%	for post in blog.get_recent_posts(5):
		<li><%include file="post.link.html.mako" args="post=post" /></li>
%	endfor
	</ul>
	<ul><caption>older</caption>
%	for month in blog.get_recent_months(5):
		<li><a href="${request.resource_url(month)}">${month.get_name()} ${month.year.number} (${month.post_count})</a></li>
%	endfor
	</ul>

	<ul><caption>stuff</caption>
		<li><a href="${request.resource_url(blog, 'post')}">Post new</a></li>
	</ul>
</nav>
</%doc>
