<%inherit file="base.html.mako" />
<h1 class="title">${Title}</h1>
%for number, post in paginator.numbered_items():
  <%include file="post.short.html.mako" args="post=post" />
%endfor
<footer>
  %if paginator.pages_total > 1:
    More posts:<br>
    %for page in paginator.page_objects():
      %if page.is_current:
      	${page.text}
      %else:
    	<a href="${page.url}">${page.text}</a>
      %endif
    %endfor
  %endif
</footer>
##% for post in posts:
##	<%include file="post.short.html.mako" args="post=post" />
##% endfor

