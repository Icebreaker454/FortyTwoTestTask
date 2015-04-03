function AsyncRequestUpdate() {
    var initial_title = $('title').text();
    var count = parseInt($('#request-table').data('count'));
    var unread = 0;
    setInterval(function() {
        var table = $('#request-table');
        $.get(
            "/requests/",
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
    }, 1000)
}


$(document).ready(function() {
    AsyncRequestUpdate();
});