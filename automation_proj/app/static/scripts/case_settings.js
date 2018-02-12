$(document).ready(function () {
	$.getJSON('/url/show', {}, function(data) {
		console.log(data.msg);
		append_tb(data, '#url-tb');
		edit();
	});
});

function append_tb(data, tb_id) {
  var tbody = document.getElementById(tb_id.substr(1));
  for (var i = 0; i < data.msg.length; i++) {
    var trow = getdatarow(data.msg[i]);
    tbody.appendChild(trow);
  }
};

function getdatarow(h){
  var row = document.createElement('tr'); //创建行
  row.setAttribute('class', 'line');

  var id = document.createElement('td');
  id.innerHTML = h.id;
  id.setAttribute('class', 'not-edit');
  id.setAttribute('data', h.id);
  row.appendChild(id);

  var desc = document.createElement('td');
  desc.innerHTML = h.desc;
  row.appendChild(desc);

  var url = document.createElement('td');
  url.innerHTML = h.url;
  row.appendChild(url);
  return row;
};

function edit() {
	$('#url-tb td[class !=not-edit ]').click(function() {
		if(!$(this).is('.input')){
			$(this).addClass('input').html('<input type="text" value="'+$.trim($(this).text())+'" />').find('input').focus().blur(function() {
				var id = $.trim($(this).parent().siblings("td:eq(0)").attr('data'));
				var name=$.trim($(this).val());
				var url = $.trim($(this).parent().attr("filed"));
				var query = new Object();
				query.id = id;
				if (name) {
					query.name = name;
				};
				if (url) {
					query.url = url;
				};
				if (name || url) {
					$.ajax({
						type: 'POST',
						url: '/url/update',
						data: JSON.stringify({
							query
						}),
						contentType: "application/json; charset=utf-8",
						dataType:'json',
						success:function(result){
							console.log(result);
						}
					});
				};
			$(this).parent().removeClass('input').html($(this).val() || 0);
		});
	}}).hover(function() {
		$(this).addClass('hover');
	},function() {
		$(this).removeClass('hover');
	});
};