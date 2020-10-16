   function startRefresh() {
    $.get('', function(data) {
        $(document.body).html(data);
    });
}
