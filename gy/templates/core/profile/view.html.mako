<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  %if done:
    <p><b>Password changed.</b></p>
  %endif
  %if failed:
    <p><b>Could not change password. ${failed}</b></p>
  %endif
  <p>
  All you can do here for now is change your password.
  <p>
  <form action="${request.route_url('core:profile')}" method="post">
    <table>
      <tr>
        <td><label for="gy:old">Current password:</td>	
        <td><input type="password" name="old" id="gy:old" required autofocus></td>
      </tr><tr>
        <td><label for="gy:new1">New password:</td>
        <td><input type="password" name="new1" id="gy:new1" required></td>
      </tr><tr>
        <td><label for="gy:new2">Again:</td>
        <td><input type="password" name="new2" id="gy:new2" required></td>
      </tr><tr>
        <td></td>
        <td><input type="submit" value="change password"></td>
      </tr>
    </table>
  </form>
</article>
