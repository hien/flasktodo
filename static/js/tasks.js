function generate_li_for_task(task) {
    var li = '<li id="'+ task.id + '"><a href="/done/' + task.id + '">X</a> ' + task.name;
    li += ' <a href="/delete/' + task.id + '" onclick="delete_task(' + task.id + '); return false;">delete</a>';
    return li;
}

function ajax_load(selector) {
    jQuery(selector).html('<img src="/static/images/loader.gif" />');

}

function delete_task(id) {
    ajax_load("#loading-" + id);
    jQuery.get('/delete/' + id + '.json',
        {},
        function (data) {
            jQuery('#task-' + id).remove();
            jQuery('#message-panel').html(data.message);
        },
    'json');
}

function add_task() {
    var name = jQuery("#task-name").val();
    jQuery("#button-add").hide();
    ajax_load("#loading-add");
    jQuery.post('/',
        {
            'format' : 'json',
            'name' : name
        },
        function (data) {
            jQuery("#button-add").show();
            jQuery("#loading-add").html('');
            jQuery("#message-panel").html(data.message);
            jQuery("#task-list").append(generate_li_for_task(data.task));
        },
    'json')
}
