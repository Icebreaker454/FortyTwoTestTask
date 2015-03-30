function AsyncRequestUpdate() {
    var initial_title = $('title').text();
    var unread = 0;
    setInterval(function() {
        var table = $('#request-table');
        var last_time = $('td:first').text();
        $.get(
            "/requests/",
            function(data){
                table.html($(data).find('#request-table'));
                table.attr("class", "table table-striped");
                if($('td:first').text() != last_time) {
                    unread++;
                    document.title = '(' + unread + ')' + initial_title;
                }
                if(document.hasFocus()){
                    unread = 0;
                }
                if(unread == 0) {
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