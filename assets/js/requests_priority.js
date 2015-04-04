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
                    $('#loading-indicator').show()
                },
                success: function (data, status) {
                    $('#loading-indicator').hide();
                },
                error: function (status, error) {
                    var row = $('#loading-indicator');
                    row.css("background-color", "red");
                    row.html('<h4>Internal server error, please, try again later</h4>');
                }
            }
        );
    });
}

function initAjaxPagination() {
    var current_page = 1;
    var page_count = $('#request-table').data('pages');
    $('#load-more-button').mouseover(function() {
        current_page++;
        if(current_page <= page_count) {
            $.ajax(
                '/requests/edit_priority/',
                {
                    dataType: 'html',
                    type: 'GET',
                    data: {
                        'page': current_page
                    },
                    beforeSend: function () {
                        $('h4 #load-more-button').hide();
                        $('#load-more').show();
                    },
                    success: function (data, status) {
                        var table_body = $(data).find('#request-table > tbody');
                        $('#request-table').append(table_body);
                        $('#load-more').hide();
                    },
                    error: function (status, error) {
                        var row = $('#loading-indicator');
                        row.css("background-color", "red");
                        row.html('<h4>Internal server error, please, try again later</h4>');
                    }
                }
            );
        }
        else {
            $('#load-more').show();
            setTimeout(function() {
                $('#load-more-button').hide();
            }, 1000);
        }
    });
}

$(document).ready(function() {
    initAjaxPagination();
    initAjaxPriorityPosting();
});