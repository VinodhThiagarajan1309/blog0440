$(document).ready(function(){
	$('#newPostForm').submit(function(event){
		$('#errTitle').text('');
		$('#errContent').text('');
		var titleString = $('#title').val().trim();
		var contentString = $('#content').val().trim();
		var validationFailed =  false;
		if(titleString.length == 0 ){
			$('#errTitle').text('Please enter title');
			validationFailed=true;
		}
		if(contentString.length == 0 ){
			$('#errContent').text('Please enter content');
			validationFailed = true
		}
		if(validationFailed){
			event.preventDefault();
		}else{
			$('#newPostForm').submit();
		}
	});
});