<%inherit file="/base.mako" />
<article>
  <h1 class="title">${Title}</h1>
  <ol>
  %for entry in entries:
    <%include file="menu_entry.html.mako" args="entry=entry, done=set([])" />
  %endfor
  </ol>
</article>
