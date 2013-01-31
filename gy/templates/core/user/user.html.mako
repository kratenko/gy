<%inherit file="/base.mako" />
<article>
  <h1>User information</h1>
  <table>
    <tr>
      <td>User:</td>
      <td>${name}</td>
    </tr><tr>
      <td>Name:</td>
      <td>${user.full_name}</td>
    </tr><tr>
      <td>Joined:</td>
      <td>${user.created.date()}</td>
    </tr>
  </table>
  
</article>
