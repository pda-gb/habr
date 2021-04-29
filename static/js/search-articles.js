$(document).ready(function (){
	$('#main-magnifier').click(function () {
		$('.form-search').fadeIn();
		$('#main-magnifier').css({
			'display':'none',
		})
		return false;
	})
	$('.magnifier-in-input').click(function(){
		$('#search-articles-form').submit();
	});
})