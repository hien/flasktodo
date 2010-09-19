function delete_task(id) {
    jQuery('#loading-' + id).html('<img src="/static/images/loader.gif" />');
    jQuery.get('/delete/' + id + '.json',
        {},
        function (data) {
            jQuery('#task-' + id).remove();
            jQuery('#message-panel').html(data.message);
        },
    'json');
}
