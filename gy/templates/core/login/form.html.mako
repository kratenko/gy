<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  %if failed:
    <h4>Login failed!</h4>
    <p>${reason}</p>
  %endif
  <form action="${request.route_url('core:login')}" method="post">
    <table>
      <tr>
        <td><label for="gy:login.name">Name:</td>	
        <td><input type="text" name="name" id="gy:login.name" autofocus required></td>
      </tr><tr>
        <td><label for="gy:login.password">Password:</td>
	<td><input type="password" name="password" id="gy:login.password" required></td>
      </tr><tr>
	<td></td>
	<td><input type="submit" value="login"></td>
      </tr>
    </table>
  </form>
  <p>
    <a href="${request.route_path('core:login.reset_password')}">Forgot your password?</a>
  </p>
  <p>
    If you don't have an account, you can <a href="${request.route_path('core:login.register')}">sign up</a>!
  </p>
</article>
