function AsyncRequestUpdate() {
    var initial_title = $('title').text();
    var unread = 0;
    var prev_count = parseInt($('#request-table').data('count'));
    setInterval(function() {
        var table = $('#request-table');
        $.get(
            "/requests/",
            function(data){
                $('#request-table').html($(data).find('#request-table'));
                var table = $('#request-table')
                var count = parseInt($(data).find('#request-table').data('count'));

                if(count != prev_count ) {
                    unread = count - prev_count;
                    if(unread != 0){
                        document.title = '(' + unread + ')' + initial_title;
                    }
                }
                if(document.hasFocus()){
                    prev_count = count;
                    document.title = initial_title;
                }
            },
            'html'
        )
    }, 1000)
}


$(document).ready(function() {
    AsyncRequestUpdate();
});