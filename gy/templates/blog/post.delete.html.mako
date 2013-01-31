<%inherit file="base.html.mako" />
<article class="gy.blog:post">
  <h1 class="title">${Title}</h1>
  <form method="post" action="${request.resource_path(post, 'delete')}">
    Confirm deletion of blog post.<br>
    <input type="submit" name=".delete" value="delete" autofocus>
    <a href="${request.resource_path(post.blog)}">cancel</a>
  </form>
  <%include file="post.short.html.mako" args="post=post" />
</article>
