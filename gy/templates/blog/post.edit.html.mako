<%inherit file="base.html.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <form action="${request.resource_url(post, 'edit')}" method="post">
  <table>
    <tr>
      <td width="1"><label for="gy.blog:edit_date">Date:</label></td>
      <td><input type="date" name="date" id="gy.blog:edit_date" value="${post.date}" maxlength="10" size="12" required></td>
    </tr>
    <tr>
      <td><label for="gy.blog:edit_title">Title:</label></td>
      <td><input type="text" name="title" id="gy.blog:edit_title" value="${post.title}" maxlength="255" size="40" required></td>
    </tr><tr>
      <td><label for="gy.blog:edit_slug">Slug:</label></td>
      <td><input type="text" name="slug" id="gy.blog:edit_slug" value="${post.slug}" maxlength="255" size="40"></td>
    </tr><tr>
      <td><label for="gy.blog:edit_published">Published:</label></td>
      <td><input type="checkbox" name="published" value="published" id="gy.blog:edit_published" ${published_checked}></td>
    </tr><tr>
      <td><label for="gy.blog:edit_content">Content:</label></td>
      <td></td>
    </tr><tr>
      <td colspan="2">
        <textarea name="content" id="gy.blog:edit_content" rows="20" cols="80">${post.content}</textarea><br>
      </td>
    </tr><tr>
      <td><label for="gy.blog:post.tags">Tags:</label>
      <td><input type="text" name="tags" id="gy.blog:post.tags" value="${post.get_item_tags_string()}" size="40"></td>
    </tr><tr>
      <td><label for="gy.blog:post.cats">Categories:</label>
      <td><input type="text" name="cats" id="gy.blog:post.cats" value="${post.get_item_categories_string()}" size="40"></td>
    </tr><tr>
      <td colspan="2">
	<input type="submit" value="post">
      </td>
    </tr>
  </table>
  </form>
</article>
