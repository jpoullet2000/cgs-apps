<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("GEMAN", "GEMAN", user) | n,unicode}
${shared.menubar(section='query')}

<link rel="stylesheet" href="/GEMAN/static/css/GEMAN.css">
<script src="/GEMAN/static/js/GEMAN.js"></script>

## Use double hashes for a mako template comment
## Main body

<div class="container-fluid">
    <div class="card">
        <h2 class="card-heading simple">Adding samples data</h2>
        <div class="card-body GEMAN">
            <div class="great-info" id="result"></div><br/><br/>

            <div class="insert-samples">
                <form action="" method="POST" name="insert-form" id="insert-form">

                    ## We display the title of each information we have to give
                    <div class="left-box">
                        % for field in q:
                            % if field == "main_title":
                                <div class="cell">
                                    <strong>${info}</strong>
                                </div>
                            % else:
                                <div class="cell">
                                    <label for="${field}">
                                        <em>${questions["sample_registration"][field]['question']}</em>
                                    </label>
                                </div>
                            % endif
                        % endfor %
                        <div class="cell">
                            <em>File related</em>
                        </div>
                    </div>
                    <div class="right-boxes">
                        <div class="right-box">
                        % for field in q:
                            % if field == "main_title":
                                <div class="cell"> </div>
                            % else:
                                % if questions["sample_registration"][field]["field"] == "text":
                                    <div class="cell">
                                        <input type="text" value="" name="%{field}" id="%{field}" maxlength="100"/>
                                    </div>
                                % elif questions["sample_registration"][field]["field"] == "select":
                                    <div class="cell">
                                        <select name="${field}">
                                        % for subid in questions["sample_registration"][field]["fields"]:
                                            <option value="${subid}">${questions["sample_registration"][field]["fields"][subid]}</option>
                                        % endfor
                                        </select>
                                    </div>
                                % elif questions["sample_registration"][field]["field"] == "date":
                                    <div class="cell">
                                        <input type="text" value"dd/mm/yy" name="${field}" id="${field}" maxlength="8"/>
                                    </div>
                                % endif
                            % endif
                        % endfor %
                            <div class="cell">
                                <select name="related_file" id="related_file">
                                    % for key, value in enumerate(files):
                                        <option value="${value}" selected>${value}</option>
                                    % endfor
                                </select>
                            </div>
                        </div>
                    </div>
                    <br/>

                    <input type="submit" value="Import" id="insertFormSubmit"/>
                    <br/>
                </form>
            </div>
        </div>
    </div>
</div>
${commonfooter(messages) | n,unicode}
