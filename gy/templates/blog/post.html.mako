<%inherit file="base.html.mako" />
<article class="gy.blog:post">
  <header>
    <h1 class="title">${post.title}</h1>
    <span class="gy.blog:posted_info">
      %if not post.published:
        <span class="gy.blog:unpublished">unpublished</span>
      %endif
      ${post.created} by <%include file="/core/user.link.mako" args="user=post.creator" />
    </span>
    %if request.has_permission('edit'):
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
    <h2 class="gy:comments"><a name="comments">Comments</a></h2>
    %for comment in post.get_recent_comments():
      <%include file="/core/comment/tree.html.mako" args="comment=comment" />
    %endfor

    <h3>Leave a comment</h3>
    <form method="post" action="">
      %if request.user is None:
      %endif
      <table>
        <tr>
	  <td width="1"><label for="gy.blog:comment.title">Title:</label></td>
	  <td width="1"><input type="text" name="title" value="Re: ${post.title}" required maxlength="255" size="40" id="gy.blog:comment.title"></td>
	</tr>
	%if request.user is None:
	 <tr>
	  <td><label for="gy.blog:comment.name">Name:</label></td>
	  <td><input type="text" name="name" required id="gy.blog:comment.name" maxlength="32" size="40"></td>
          <td><i>(Maybe <a href="${request.route_path('core:login')}">login</a>?)</i></td>
	 </tr><tr>
	  <td><label for="gy.blog:comment.email">Email:</label></td>
	  <td><input type="email" name="email" required id="gy.blog:comment.email" maxlength="255" size="40">
	  <td><i>won't show</i></td>
	 </tr>
	%endif
	<tr>
	  <td><label for="gy.blog:comment.content">Text:</label></td>
	  <td></td><td></td>
	</tr>
	<tr>
	  <td colspan="3">
            <textarea name="content" required cols="80" rows="20" id="gy.blog:comment.content"></textarea>
	  </td>
	</tr><tr>
	  <td colspan="2">
            <input type="submit" name=".post_comment" value="post comment">
	  </td>
	  <td></td>
	</tr>
      </table>
    </form>
  </footer>
</article>
