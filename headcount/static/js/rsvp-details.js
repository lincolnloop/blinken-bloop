$(document).ready(function(){
    $('.notes-all').hide();

    $('.rsvp-table').on('click', '.notes-truncated', function(e){
        e.preventDefault();
        $('#notes-' + $(this).parents('tr').attr('id').slice(5)).toggle(300);
    });
});