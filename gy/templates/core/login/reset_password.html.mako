<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <p>If you lost your password, we can send a new one
     to the email address you registered for your account,
     just give us the login name.
  </p>
  <form action="${request.route_path('core:login.reset_password')}" method="post">
    <table>
      <tr>
        <td><label for="gy:login.name">Name:</td>	
         <td><input type="text" name="name" id="gy:login.name" autofocus required></td>
      </tr><tr>
        <td></td>
        <td><input type="submit" value="reset"></td>
      </tr>
    </table>
  </form>
</article>
