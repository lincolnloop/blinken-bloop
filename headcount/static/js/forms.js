$(document).ready(function(){
    $('.dateinput').attr('placeholder', '   /   /       ');
    $('.timeinput').attr('placeholder', '   :       ');


    $('.no-horizontal').find('.col-lg-2').removeClass('col-lg-2').addClass('col-lg-12');
    $('.no-horizontal').find('.col-lg-2').removeClass('col-lg-2').addClass('col-lg-12');

    var maxGuests = $($('.max-guests')[0]).attr('id').slice(4);
    if (parseInt(maxGuests, 10) > 0) {
        $('#id_num_guests').attr('max', maxGuests);
    }
});