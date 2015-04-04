function AsyncRequestUpdate() {
    var initial_title = $('title').text();
    var count = parseInt($('#request-table').data('count'));
    var unread = 0;
    var data_str;

    if(location.href.indexOf('reverse') >= 0)
    {
        data_str = {'reverse':1}
    }

    setInterval(function() {
        var table = $('#request-table');
        $.ajax(
            '/requests/',
            {
                type: 'GET',
                data: data_str,
                success:function(data){
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
                dataType:'html'
            }
        );
    }, 1000);
}


$(document).ready(function() {
    AsyncRequestUpdate();
});