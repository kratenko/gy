<%inherit file="/base.mako" />
<article class="gy:page">
  <h1 class="title">${Title}</h1>
  <form action="${request.resource_url(parent_page, 'new')}" method="post">
  <table>
    <tr>
      <td width="1"><label for="gy:new_title">Title:</label></td>
      <td><input type="text" id="gy:new_title" name="title" maxlength="255" size="40" value="${title}" required autofocus></td>
    </tr><tr>
      <td><label for="gy:new_slug">Slug:</label></td>
      <td><input type="text" id="gy:new_slug" name="slug" maxlength="255" size="40" value="${slug}"></td>
    </tr><tr>
      <td><label for="gy:new_content">Content:</label></td>
      <td></td>
    </tr><tr>
      <td colspan="2">
	<textarea name="content" id="gy:new_content" cols="80" rows="20">${content}</textarea>
      </td>
    </tr><tr>
      <td colspan="2">
        <input type="submit" value="save">
	<a href="${request.resource_url(parent_page)}">abort</a>
      </td>
    </tr>
  </table>
  </form>
</article>
