$(document).ready(function(){
    $('.dateinput').attr('placeholder', '   /   /       ');
    $('.timeinput').attr('placeholder', '   :       ');


    $('.no-horizontal').find('.col-lg-3').removeClass('col-lg-3').addClass('col-lg-12');
    $('.no-horizontal').find('.col-lg-3').removeClass('col-lg-3').addClass('col-lg-12');

    var maxGuests = $($('.max-guests')[0]).attr('id').slice(4);
    if (parseInt(maxGuests, 10) > 0) {
        $('#id_num_guests').attr('max', maxGuests);
    }

    $('#div_id_response').on('change', 'input[name=response]', function (){
        if ($(this).attr('value') == 'no') {
            $('#div_id_num_guests').hide(300);
        } else {
            $('#div_id_num_guests').show(300);
        }
    });
});