   function startRefresh() {
    $.get('', function(data) {
        $(document.body).html(data);
    });
}
$(function() {
    setTimeout(startRefresh,10000);
});

