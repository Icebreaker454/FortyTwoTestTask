function AsyncRequestUpdate() {
    var initial_title = $('title').text();
    var count = parseInt($('#request-table').data('count'));
    var unread = 0;
    var url;


    setInterval(function() {
            if ($(location.search.substr('reverse'))){
        url = "/requests/";
    }
    else {
        url = ("/requests/?reverse=1");
    }
        var table = $('#request-table');
        $.get(
            url,
            function(data){
                table.html($(data).find('#request-table'));
                table.attr("class", "table table-striped");
                var new_count = parseInt($(data).find('#request-table').data('count'));
                if(new_count > count) {
                    unread = new_count - count;
                    document.title = '(' + unread + ')' + initial_title;
                }
                if(document.hasFocus()){
                    unread = 0;
                    document.title = initial_title;
                    count = new_count;
                }
            },
            'html'
        )
    }, 1000);
        $('input[type="number"]').change(function () {
            $.ajax(
                '/requests/',
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

                    },
                    success: function (data, status) {
                        alert(status);
                    },
                    error: function (status, error) {
                        alert(error);
                    }
                }
            );
        });
    }
}


$(document).ready(function() {
    AsyncRequestUpdate();
});