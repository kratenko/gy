<%inherit file="/base.mako" />
<article>
  <h1>Item information</h1>
  <table>
    <tr>
      <td>id:</td>
      <td>${id}</td>
    </tr><tr>
      <td>type:</td>
      <td>${item.type}</td>
    </tr><tr>
      <td>Signature</td>
      <td>${item.signature()}:</td>
    </tr><tr>
      <td>Short</td>
      <td>${item.short()}:</td>
    </tr>
  </table>
  
</article>
