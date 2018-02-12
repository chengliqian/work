$(function () {
	$.getJSON('/dashboard/overview', {}, function(data) {
		$('#users').text(data.msg.user_count);
		$('#cases').text(data.msg.case_count)
	});
});