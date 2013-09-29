$(document).ready(function(){
    $('.notes-all').hide();

    console.log(window.location.hash);

    $('.rsvp-table').on('click', '.notes-truncated', function(e){
        e.preventDefault();
        $('#notes-' + $(this).parents('tr').attr('id').slice(5)).toggle(300);
    });

    if (window.location.hash) {
        $(window.location.hash).addClass('highlight');
        $('#notes-' + window.location.hash.slice(6)).addClass('highlight').toggle();
    }
});