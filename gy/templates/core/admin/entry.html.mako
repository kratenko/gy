<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <form method="post">
    <table>
      <tr>
        <td width="1">number:</td>
	<td><input type="number" name="number" value=""/></td>
      </tr>
    </table>
  </form>
</article>
