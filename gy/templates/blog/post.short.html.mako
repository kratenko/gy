<%page args="post" />
<article class="gy.blog:post.outline">
  <header>
    <h2 class="gy.blog:title"><a href="${request.resource_url(post)}" class="blog blog:view">${post.title}</a></h2>
    <span class="gy.blog:posted_info">
      %if not post.published:
        <span class="gy.blog:unpublished">unpublished</span>
      %endif
      ${post.created} by
      <%include file="/core/user.link.mako" args="user=post.creator" />
    </span>
    %if request.has_permission('edit', post):
      <span class="gy.blog:edit_link">
        <a href="${request.resource_url(post, 'edit')}">edit</a>
        <a href="${request.resource_url(post, 'delete')}">delete</a>
      </span>
    %endif
  </header>

  ${post.render_content()|n}

  <footer>
    <span class="gy:categories">
      Posted in:
      %for category in post.categories:
        <%include file="/core/a/category.mako" args="category=category, app=blog" />
      %endfor
    </span>
    <br>
    <span class="gy:tags">
      Tags:
      %for tag in post.tags:
        <%include file="/core/a/tag.mako" args="tag=tag, app=blog" />
      %endfor
    </span>
    <br>
    ## Comments:
    <a href="${request.resource_url(post, anchor='comments')}">
      %if len(post.item_comments) == 0:
        no comments yet
      %elif len(post.item_comments) == 1:
        1 comment
      %else:
        ${len(post.item_comments)} comments
      %endif
    </a>
  </footer>
</article>
