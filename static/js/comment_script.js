$(document).ready(function (event) {
    $('.reply-btn').click(function() {
        $(this).parent().next('.replied-comments').fadeToggle()
    });
    /*
    $(document).on('submit', '.comment-form', function(event){
        event.preventDefault(); 
        $.ajax({
            type: 'POST', 
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
             $('.main-comment-section').html(response['form']);
            },
            error: function(rs, e) {
             console.log(rs.responseText);
            }
        }); 
     });
     */
});
