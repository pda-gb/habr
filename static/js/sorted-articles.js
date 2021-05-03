$(document).ready(function () {
    $('.sorted-menu').click(function () {
        $('#form-sorted').css({
            'display': 'block',
        });
    })
    $(document).click(function(e) {
        if (!$(e.target).is('.sorted-icon')
        && !$(e.target).is('.sorted-input')
        && !$(e.target).is('.sorted-list')
        && !$(e.target).is('.sorted-label')
        && !$(e.target).is('.sorted-elem')) {
            $('#form-sorted').css({
                'display': 'none',
            });
        }
    })
    $('.sorted-input').click(function(){
        $('#form-sorted').submit();
    })
})