<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  %if request.user:
    <p>You are already loged in. To register a new user, you must 
    first <a href="${request.route_url('core:login.out')}">log out</a>.</p>
  %else:
    <form action="${request.route_url('core:login.register')}" method="post">
      <h4>Hello new user.</h4>
      <p>
        If you want to join ${request.site.title}, please fill 
        out the form on this page. The password needed to log in 
	will be sent to the email address you specify here.
      </p>
      <table>
        <tr>
	  <th>User name:</th>
	  <td><input type="text" name="name" required pattern="[a-z][a-z0-9]{2,15}" autofocus></td>
	  <td>User your choose to identify yourself.</td>
	</tr><tr>
	  <th>Full name:</th>
	  <td><input type="text" name="full_name" required></td>
	  <td>Your name. So others can identify you, or know kow to address you.</td>
	</tr><tr>
	  <th>Email&nbsp;address:</th>
	  <td><input type="email" name="email" required></td>
	  <td>Make sure you it is correct.</td>
	</tr><tr>
	  <td colspan="2"><input type="submit" value="create user"></td>
	</tr>
      </table>
    </form>
  %endif
</article>
