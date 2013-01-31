<%inherit file="/base.mako" />
<article class="gy:page">
  <h1 class="title">${Title}</h1>
  <form action="${request.resource_url(page, 'edit')}" method="post">
  <table>
    <tr>
      <td width="1"><label for="gy:edit_title">Title:</label></td>
      <td><input type="text" id="gy:edit_title" name="title" maxlength="255" size="40" value="${page.title}" required></td>
    </tr><tr>
      <td><label for="gy:edit_slug">Slug:</label></td>
      <td><input type="text" id="gy:edit_slug" name="slug" maxlength="255" size="40" value="${page.slug}" required></td>
    </tr><tr>
      <td><label for="gy:edit_content">Content:</label></td>
      <td></td>
    </tr><tr>
      <td colspan="2">
	<textarea name="content" id="gy:edit_content" cols="80" rows="20">${page.content}</textarea>
      </td>
    </tr><tr>
      <td colspan="2">
        <input type="hidden" name="id" value="${page.id}">
        <input type="submit" value="save">
	<a href="${request.resource_url(page)}">abort</a>
      </td>
    </tr>
  </table>
  </form>
</article>
