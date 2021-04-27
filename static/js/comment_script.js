$(document).ready(function(){
    $(".reply").on('click', function(){
        var parentId = $(this).attr('data-id')
        $("#createChildCommentForm-"+parentId).fadeToggle();
    });
    $('#createCommentBtn').click(function(e) {
        e.preventDefault()
        let content = $('#createCommentForm').serialize();

        $.ajax({
            url: $("#createCommentForm").data('url'),
            data: content,
            type: 'POST',
            success: function(response) {
                $('#commentArticle').html(response.result);
            }
        })
    })
});
