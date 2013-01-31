<%page args="entry, done" />
<li>
  ${entry.link_text} ${entry.target.signature()}, ${entry.target.short()}
  <a href="${request.route_url('core:admin.menu_entry', _query={'menu':entry.menu_id,'number':entry.number})}">edit entry</a>
  %if hasattr(entry.target, 'menu_entries') and entry.target_id not in done:
    <ol>
    %for subentry in entry.target.menu_entries:
      <%include file="menu_entry.html.mako" args="entry=subentry, done=done.union([entry.target_id])" />
    %endfor
    </ol>
  %endif
</li>
