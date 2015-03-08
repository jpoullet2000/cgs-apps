
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar navbar-inverse navbar-fixed-top nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="currentApp">
              <a href="/genomicAPI">
                <img src="/genomicAPI/static/art/icon_genomicAPI_48.png" class="app-icon" />
                Genomicapi
              </a>
             </li>
             <li class="${is_selected(section, 'index')}"><a href="/GEMAN/">Index</a></li>
             <li class="${is_selected(section, 'query')}"><a href="/GEMAN/query/index/interface/">Query</a></li>
             <li class="${is_selected(section, 'sample')}"><a href="/GEMAN/sample/index/interface/">Query</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
