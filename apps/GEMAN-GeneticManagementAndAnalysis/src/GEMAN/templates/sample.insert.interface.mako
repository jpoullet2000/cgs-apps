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
                        {strict: true,allowInvalid: false},
                    % else:
                        % if questions["sample_registration"][field]["field"] == "text":
                            {strict: true},
                        % elif questions["sample_registration"][field]["field"] == "select":
                            {type: 'autocomplete', source: [
                                    % for subid in questions["sample_registration"][field]["fields"]:
                                        '${questions["sample_registration"][field]["fields"][subid]}',
                                    % endfor
                               ], strict: true, allowInvalid: false},
                        % elif questions["sample_registration"][field]["field"] == "date":
                            {type: 'date', dateFormat: 'MM/DD/YYYY', correctFormat: true, strict: true,allowInvalid: false},
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

        //The simple getData remove empty cell, which is not very practical...
        //Each line will be separated by a ';' and each cell by a ','
        var completeData = "";
        var currentCellData = "";
        for(var x=0; x < hot.countRows(); x++) {
            for(var y=0; y < hot.countCols(); y++) {
                if(y > 0)
                    completeData += ",";
                currentCellData = hot.getDataAtCell(x, y)

                if(currentCellData !== undefined)
                    completeData += currentCellData;
            }
            completeData += ";"
        }

        $('#vcf_data').val(completeData);
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

                    <!-- If we already got the form, we display the result-->
                    % if result:
                        % if result['status'] != 1:
                            <strong><font color="red">${result['error']}</font></strong>
                        % else:
                            <strong><font color="green">Data correctly added</font></strong>
                        % endif
                    % endif
                    <br/>
                    <div id="example" class="handsontable"></div>
                    <br/>
                    <input type="text" value="" id="vcf_data" name="vcf_data" style="display:none"/>
                    <input type="submit" value="Import" id="save-handson"/>
                    <br/>
                </form>
                % endif
            </div>
        </div>
    </div>
</div>
${commonfooter(messages) | n,unicode}
