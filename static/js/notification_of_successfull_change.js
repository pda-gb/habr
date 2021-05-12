$('.container').on('click', '.save-changes', function (event) {

    $.ajax({
        url: "/account/edit_profile/edit_password/",
        success: function (data) {
            $('.container').html(data.result);
//            alert('Данные успешно сохранены!');
            $('.alert').css('display', 'block');
            console.log('success');
        },
    });
    event.preventDefault();
});