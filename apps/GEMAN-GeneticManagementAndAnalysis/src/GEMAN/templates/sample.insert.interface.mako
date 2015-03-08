<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

<script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>

<script src="http://handsontable.com/dist/handsontable.full.js"></script>
<script src="http://handsontable.com/demo/js/moment/moment.js"></script>
<script src="http://handsontable.com/demo/js/pikaday/pikaday.js"></script>
<link rel="stylesheet" media="screen" href="http://handsontable.com/dist/handsontable.full.css">
<link rel="stylesheet" media="screen" href="http://handsontable.com/demo/js/pikaday/css/pikaday.css">
<link rel="stylesheet" media="screen" href="http://handsontable.com/demo/css/samples.css">

<script>
$(document).ready(function () {
    var data = [
            % if not error_sample:
                % for key, value in enumerate(samples):
                    ['${value}'],
                % endfor
            % endif
            ],
    container = document.getElementById('example'),
    hot;

    hot = new Handsontable(container, {
        data: data,
        minSpareRows: 1,
        maxRows: ${samples_quantity},
        maxCols: 10,
        colHeaders: [
        % for field in q:
            % if field == "main_title":
                '${questions["sample_registration"][field]}',
            % else:
                '${questions["sample_registration"][field]['question']}',
            % endif
        % endfor %
                ],
        colWidths: [100, 130, 100, 100, 100, 150, 150, 150, 200, 220],
        contextMenu: true,
        columns: [
                % for field in q:
                    % if field == "main_title":
                        {},
                    % else:
                        % if questions["sample_registration"][field]["field"] == "text":
                            {},
                        % elif questions["sample_registration"][field]["field"] == "select":
                            {type: 'autocomplete', source: [
                                    % for subid in questions["sample_registration"][field]["fields"]:
                                        '${questions["sample_registration"][field]["fields"][subid]}',
                                    % endfor
                               ], strict: false},
                        % elif questions["sample_registration"][field]["field"] == "date":
                            {type: 'date', dateFormat: 'MM/DD/YYYY', correctFormat: true},
                        % endif
                    % endif
                % endfor %
        ],
        cells: function (row, col, prop) {
            var cellProperties = {};

            if (col === 0 || this.instance.getData()[row][col] === 'readOnly') {
              cellProperties.readOnly = true; // make cell read-only if it is first row or the text reads 'readOnly'
            }

            return cellProperties;
        }
    });


    $("#handson-form").submit(function(e){
        alert(hot.getData());
        $('#handson-data').val(hot.getData());
    });


    });
</script>


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
                <form action="" method="POST" name="insert-form" id="handson-form">
                % if error_get:
                    <strong><font color="red">You have to give a vcf file!</font></strong>
                % elif error_sample:
                    <strong><font color="red">We have found no sample information in the vcf. <br/>The file may be corrupted or the format not taken into account in the current version of the code.</font></strong>
                % else:
                    <div id="example" class="handsontable"></div>

                    <!-- If we already got the form, we display the result-->
                    % if result:
                        % if result['status'] != 1:
                            <strong><font color="red">${result['error']}</font></strong>
                        % else:
                            <strong><font color="green">Data correctly added</font></strong>
                        % endif
                    % endif
                    <br/><br/>
                    <!-- We display the title of each information we have to give-->

                    <!-- NOT USED ANYMORE (we just let the code in case we would need it)
                    <div class="left-box">
                        % for field in q:
                            % if field == "main_title":
                                <div class="cell">
                                    <strong>${questions["sample_registration"][field]}</strong>
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
                                            <input type="text" value="" name="${field}" id="${field}" maxlength="100"/>
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
                    </div>-->
                    <br/>
                    <input type="text" value="" id="handson-data" style="display:none"/>
                    <input type="submit" value="Import" id="save-handson"/>
                    <br/>
                </form>
                % endif
            </div>
        </div>
    </div>
</div>
${commonfooter(messages) | n,unicode}
