<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <p>Do you really want to delete this item? It cannot be undone:</p>
  <p>${item.signature()}</p>
  <form method="post">
    <input type="submit" name=".delete_item" value="delete item">
  </form>

