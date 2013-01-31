<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>

%if request.admin_active():
  <p>Admin functionallity is allready acitvated.</p>
%elif request.user.is_admin:
  %if failed:
    <p>The password you specified was not correct.</p>
  %endif
  <form action="${request.route_url('core:admin.activate')}" method="post">
    <table>
      <tr>
        <td colspan="2">
          Please verify that it is still youself.
        </td>
      </tr>
      <tr>
	<td><label for="gy:password">Password:</label></td>
	<td><input type="password" id="gy:password" name="password" autofocus required></td>
      </tr>
      <tr>
        <td></td>
        <td><input type="submit" value="activate admin"></td>
      </tr>
    </table>
  </form>
%else:
  <p>You may not do that.</p>
%endif
</article>
