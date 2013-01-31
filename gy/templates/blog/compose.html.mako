<%inherit file="base.html.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <form action="/blog/post" method="post">
  ##<form action="${request.resource_url(blog, 'post')}" method="post">
  <table>
    <tr>
      <td width="1"><label for="gy.blog:post.date">Date:</label></td>
      <td><input type="date" name="date" id="gy.blog:post.date" value="${date}"></td>
    </tr><tr>
      <td><label for="gy.blog:post.title">Title:</label></td>
      <td><input type="text" name="title" id="gy.blog:post.title" value="${title}" required autofocus></td>
    </tr><tr>
      <td><label for="gy.blog:post.slug">Slug:</label></td>
      <td><input type="text" name="slug" id="gy.blog:post.slug" value="${slug}"></td>
    </tr><tr>
      <td><label for="gy.blog:post.published">Published:</label></td>
      <td><input type="checkbox" name="published" value="published" ${published_checked}></td>
    </tr><tr>
      <td><label for="gy.blog:post.content">Content:</label></td>
      <td></td>
    </tr><tr>
      <td colspan="2">
	<textarea name="content" id="gy.blog:post.content" rows="20" cols="80">${content}</textarea>
      </td>
    </tr><tr>
      <td><label for="gy.blog:post.tags">Tags:</label>
      <td><input type="text" name="tags" id="gy.blog:post.tags" value="${tags}" size="40"></td>
    </tr><tr>
      <td><label for="gy.blog:post.cats">Categories:</label>
      <td><input type="text" name="cats" id="gy.blog:post.cats" value="${cats}" size="40"></td>
    </tr><tr>
      <td colspan="2">
	<input type="submit" value="post">
      </td>
    </tr>
  </table>
</form>
</article>
