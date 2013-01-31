<%page args="comment" />
<article class="gy:comment">
  <header>
    <h3>${comment.title}</h3>
    <span class="gy.blog:posted_info">
      %if comment.poster_name:
        ${comment.created} by <u>${comment.poster_name}</u> (anonymous)
      %else:
        ${comment.created} by 
        <%include file="/core/user.link.mako" args="user=comment.creator" />
      %endif
    </span>
    %if request.has_permission('admin', comment):
      <span class="gy.blog:edit_link">
        <a href="${request.route_path('core:admin.delete', id=comment.id)}">delete comment</a>
      </span>
    %endif
  </header>
  ${comment.render_content()|n}
</article>
