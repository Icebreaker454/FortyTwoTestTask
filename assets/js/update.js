/**
 * Created by icebreaker on 28.03.15.
 */
function initEditPage() {
    $('form').ajaxForm({
        dataType: 'json',
        beforeSubmit: function () {
            $('input').attr("disabled", "disabled");
            $('textarea').attr("disabled", "disabled");
            window.scrollTo(0, 0);
            $('#loading-indicator').show();
            $('div[class="spinner"]').show();
        },
        success: function (data, status, xhr) {
            $('div[class="spinner"]').hide();
            $('.alert-success').html("<h3>Form submitted</h3>");
            setTimeout(function() {
                 $('#loading-indicator').hide();
                 $('input').removeAttr("disabled");
                 $('textarea').removeAttr("disabled");
            }, 3000);
        }
    });

    return false;
}

function initDateFields() {
    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD'
         }).on('dp.hide', function(event) {
            $(this).blur();
        });
}

$(document).ready(function(){
    initEditPage();
    initDateFields();
});