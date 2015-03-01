<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("Genomicapi", "genomicAPI", user) | n,unicode}
${shared.menubar(section='query')}

<link rel="stylesheet" href="/genomicAPI/static/css/genomicAPI.css">
<script src="/genomicAPI/static/js/genomicAPI.js"></script>

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
  <div class="card">
    <h2 class="card-heading simple">Insert/Upload Data</h2>
    <div class="card-body genomicAPI">
      <div class="great-info" id="result"></div><br/><br/>
            
      <form action="" method="POST" class="insertForm" name="insertForm" id="insertForm">
        <div class="left-box">
          <label for="import_file">File to import: </label>
        </div>
        <div class="right-box">
          <select name="import_file" id="import_file">
            % for key, value in enumerate(filesList):
              <option value="${value}" selected>${value}</option>
            % endfor
          </select>
        </div>
        <br/>
        <div class="left-top-box">
          <label for="samples_ids">Samples ids (one on each line): </label>
        </div>
        <div class="right-box">
          <textarea rows="5" name="samples_ids" id="samples_ids" cols="5" maxlength="30000"></textarea>
        </div>
        <br/>
                        
        <input type="submit" value="Import" id="insertFormSubmit"/>
        <br/>       
      </form>
      
    </div>
  </div>
</div>
${commonfooter(messages) | n,unicode}
