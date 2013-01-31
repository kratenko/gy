<%inherit file="/base.mako" />
<article class="gy:page">
  <header>
    <h1 class="title">${Title}</h1>
    <span class="gy:edit_item">
      <a href="${request.resource_path(page)}">view</a>
    </span>
  </header>
  <h2>Info</h2>
  <table>
    <tr>
      <td>Item:</td>
      <td>${page.signature()}</td>
    </tr><tr>
      <td>Parent:</td>
      %if parent is None:
        <td>None</td>
      %else:
        <td>${page.parent.signature()}</td>
      %endif
    </tr>
  </table>

  <h2>Actions</h2>
  <form method="post">
    Delete: <input name=".delete_page" type="submit" value="delete page" onclick="return confirm('Are you sure, you want to delete this page? It cannot be undone.');">
  </form>
  <form method="post">
    Move to <input name="new_parent" type="number" placeholder="new parent id">
    <input type="submit" name=".move_page" value="move">
  </form>

  <h2>Permissions</h2>
  <form method="post">
    <ul>
      %for permission in page.permissions:
        <li>
          <input type="checkbox" name="permission" value="${permission.auth_id}.${permission.permission}">
      	  ${permission.auth.signature()} 
          may &lt;${permission.permission}&gt;
        </li>
      %endfor
    </ul>
    <input name=".remove_permission" type="submit" value="remove">
  </form>
  <br>
  <form method="post">
    <h3>Add permissions</h3>
    grant <input type="text" maxlength="16" name="permission" size="16" required placeholder="permission">
    to <input type="number" min="1" name="auth" title="Group-id or User-id" required size="5" placeholder="User-/Group-ID">
    <input type="submit" value="add permission" name=".add_permission">
  </form>
</article>
