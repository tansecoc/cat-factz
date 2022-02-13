// https://pythonprogramming.net/jquery-flask-tutorial/
$(function(){
	$('button').click(function(){
		$.ajax({
			url: '/',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});