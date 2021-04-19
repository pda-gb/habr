/*$(document).ready(function (event) {
    $('.reply-btn').click(function() {
        $(this).parent().next('.replied-comments').fadeToggle()
    });
    
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
     
});*/

$(document).ready(function(){
    $(".reply").on('click', function(){
        var parentId = $(this).attr('data-id')
        $("#form-"+parentId).fadeToggle();
    })
    $(".submit-reply").on('click', function(e){
        e.preventDefault()
        var parentId = $(this).attr('data-submit-reply')
        var id = $(this).attr('data-id')
        var text = $('#form-'+id).find('textarea[name="comment-text"]').val();
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');
        data = {
            user: "{{ request.user.username }}",
            parentId: parentId,
            text: text,
            id: id,
            csrfmiddlewaretoken: csrftoken
        }
    })
});
