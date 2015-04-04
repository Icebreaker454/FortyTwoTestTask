/**
 * Created by icebreaker on 04.04.15.
 */
function initAjaxPriorityPosting() {
    $('input[type="number"]').change(function () {
        $.ajax(
            '/requests/edit_priority/',
            {
                dataType: 'json',
                async: true,
                type: 'POST',
                data: {
                    'pk': $(this).data('request-id'),
                    'priority': $(this).val(),
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                beforeSend: function () {
                    $('.spinner').show()
                },
                success: function (data, status) {
                    $('.spinner').hide();
                },
                error: function (status, error) {
                    var row = $('#loading-row');
                    row.css("background-color", "red");
                    row.html('<h4>Internal server error, please, try again later</h4>');
                }
            }
        );
    });

}

$(document).ready(function() {
   initAjaxPriorityPosting();
});