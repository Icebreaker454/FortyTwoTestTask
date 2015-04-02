/**
 * Created by icebreaker on 28.03.15.
 */

function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function initEditPage() {
    $('form').ajaxForm({
        dataType: 'json',
        beforeSubmit: function () {
            if($('#picture-clear_id').is(':checked')) {
                $('form .clearablefileinput').clearFields();
            }
            $('input').attr("disabled", "disabled");
            $('textarea').attr("disabled", "disabled");
            $('#loading-indicator').show();
            $('div[class="spinner"]').show();
        },
        success: function (data, status) {
            if(data.url) {
                $(location).attr('href', data.url)
            }
            else {
                $('div[class="spinner"]').hide();
                $('.alert-success').html("<h3>Form submitted! <a href='/'> Go to main page</a></h3>");
                $('input').removeAttr("disabled");
                $('textarea').removeAttr("disabled");
            }
        }
    });

    $("#id_picture").change(function(){
        readURL(this);
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