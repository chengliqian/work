// 复选框全选、反选
$(document).ready(function () {
  $('#checkall').click(function () {
    if ($(this).prop('checked')) {
      $('tbody :checkbox').prop('checked', true);
    } else {
      $('tbody :checkbox').prop('checked', false);
    }
  });
});

$(document).ready(function() {
  $('#exc-checked').click(function() {
    var case_values = new Array();
    $("input[name='case']:checked").each(function() {
      case_values.push(this.value)
    });
    if (case_values.length == 0) {
      var result = confirm('请勾选需要执行的用例');
      if(result){
        return;
      } else {
        return;
      };
    };
    $(this).button('loading');
    $.ajax({
      url: '/case/exc',
      type: 'POST',
      data: JSON.stringify({
        ids: case_values
      }),
      contentType: "application/json; charset=utf-8",
      success: function(data) {
        alert(data.msg);
      }
    });
  });
});

$(document).ready(function() {
  $('#exc-all').click(function() {
    $(this).button('loading');
    $(this).button('reset');
    console.log(3333);
  });
});

$(document).ready(function() {
  $('#save-modal').click(function() {
    clear_modal_data();
  });
});

$(document).ready(function() {
  $('#close-modal').click(function() {
    clear_modal_data();
  });
});

$(document).ready(function() {
  $('#close-show-modal').click(function() {
    clear_show_modal();
  });
});

function show_case(obj){
  var id = $(obj).attr("value");
  $.getJSON($SCRIPT_ROOT + '/case/show-case', {
    id: id
  },
  function(data) {
    console.log(data.msg);
    if(isJsonStr(data.msg['expectation'])){
      var s2 = eval('('+data.msg['expectation']+')');
      var req_expc = library.json.prettyPrint(s2);
      $("#request-expection").html(req_expc);
    }else{
      $("#request-expection").html(data.msg['expectation']);
    }
    if(isJsonStr(data.msg['request_data'])){
      console.log('test1');
      var s1 = eval('('+data.msg['request_data']+')');
      var req_data = library.json.prettyPrint(s1);
      $("#request-data").html(req_data);
    }else{
      console.log('test2');
      $("#request-data").html(data.msg['request_data']);
    }
      // var s1 = eval('(' + data.msg['request_data'] + ')');
      // var req_data = library.json.prettyPrint(s1);
      // if (isJsonStr(data.msg['expectation'])) {
      //   var s2 = eval('(' + data.msg['expectation'] + ')');
      //   var req_expc = library.json.prettyPrint(s2);
      //   $("#request-expection").html(req_expc);
      // } else {
      //   $("#request-expection").html(data.msg['expectation']);
      // };
      //$("#request-data").html(req_data);
      $("#request-url").html(data.msg['url']);
      $("#request-desc").html(data.msg['desc']);
      $("#request-type").html(data.msg['request_type']);
      $("#request-name").html(data.msg['name']);
      $("#request-id").html(data.msg['id']);
  }); 
};

function isJsonStr(str) {
  try {
    if (typeof JSON.parse(str) == "object") {
      return true;
    }
  } catch(e) {
  }
  return false;
};

function update_case(obj){
  var id = $(obj).attr("value");
  $.getJSON($SCRIPT_ROOT + '/case/show-case', {
    id: id
  },
  function(data) {
    console.log(data.msg);
    $('#update-id').val(data.msg['id']);
    $('#update-name').val(data.msg['name']);
    $('#update-url').val(data.msg['url']);
    $('#update-desc').val(data.msg['desc']);
    $('#update-data').val(data.msg['request_data']);
    $('#update-expectation').val(data.msg['expectation']);
    if (data.msg['request_type']=='post') {
      // document.getElementById('update-post').checked = true;
      $('#update-post').attr('checked', true);
    } else {
      // document.getElementById('update-get').checked = true;
      $('#update-get').attr('checked', true);
    };
  });
};

function clear_modal_data(){
  $('#new').on('hidden.bs.modal', function () {
    $('#add-name').val('');
    $('#add-desc').val('');
    $('#add-url').val('');
    $('#add-data').val('');
    $('#add-expectation').val('');
    document.getElementById('add-post').checked = false;
    document.getElementById('add-get').checked = false;
  });
};

function clear_show_modal(){
  $('#show').on('hidden.bs.modal', function() {
    $('#request-id').empty();
    $('#request-url').empty();
    $('#request-name').empty();
    $('#request-desc').empty();
    $('#request-type').empty();
    $('#request-expection').empty();
    $('#request-data').empty();
    $('#response-data').empty();
    $('#awaiting').html('Awaiting request...');
  });
};

$(document).ready(function () {
  $('#update-post').click(function() {
    // document.getElementById('update-post').checked = true;
    $('#update-post').attr('checked', true);
    $('#update-get').attr('checked', false);
  });
  $('#update-get').click(function() {
    $('#update-post').attr('checked', false);
    $('#update-get').attr('checked', true);
  });
});

function edit_case(obj){
  var id = $('#update-id').val();
  var name = $('#update-name').val();
  var desc = $('#update-desc').val();
  var curl = $('#update-url').val();
  var data = $('#update-data').val();
  var expectation = $('#update-expectation').val();
  if ($('#update-post').attr('checked') == 'checked') {
    var type = 'post'
  };
  if ($('#update-get').attr('checked') == 'checked') {
    var type = 'get'
  };
  console.log(type);
  $.ajax({
    url: '/case/update',
    type: 'POST',
    data: JSON.stringify({
      id: id,
      name: name,
      desc: desc,
      url: curl,
      request_data: data,
      request_type: type,
      expectation: expectation
    }),
    contentType: "application/json; charset=utf-8",
    success: function(data) {
      alert(data.msg);
    }
  });
};

function add_case(){
  // var data = $('#new').data();
  var name = $('#add-name').val();
  var desc = $('#add-desc').val();
  var curl = $('#add-url').val();
  var data = $('#add-data').val();
  var expectation = $('#add-expectation').val();
  if ($('#add-post :checked')) {
    var type = 'post';
  } else if ($('#add-post :checked')) {
    var type = 'get';
  } else {
    var type = '';
  };
  if (!type) {
    console.log('dfddf');
  };
  // console.log(data);
  if (!name || !desc || !curl || !data || !expectation || !type) {
    var result = confirm('不允许为空');
    if(result){
        return false;
    }else{
        return false;
    }
  };
  $.post('/nex-api/add', {
    name: name,
    desc: desc,
    curl: curl,
    data: data,
    type: type,
    expectation: expectation
    },
    function(data) {
      alert(data.msg);
  });
};

function send_case(obj){
  var id = $('#request-id').text();
  $.ajax({
    url: '/case/send',
    type: 'POST',
    data: JSON.stringify({id: id}),
    contentType: "application/json; charset=utf-8",
    success: function(data) {
    $('#awaiting').empty();
    var data = library.json.prettyPrint(data.msg);
    console.log(data);
    $('#response-data').html(data);
    }
  });
};

function del_case(obj){
  var id = $(obj).attr("value");
  $.ajax({
    url: '/case/delete',
    type: 'POST',
    data: JSON.stringify({id: id}),
    contentType: "application/json; charset=utf-8",
    success: function(data) {
      alert(data.msg);
    }
  });
};

function del_confirm(obj){
    var result = confirm('删除后无法恢复，请谨慎操作');
    if(result){
        del_case(obj);
    }else{
        return false;
    }
};

function sleep(d){
  for(var t = Date.now();Date.now() - t <= d;);
};

if (!library)
   var library = {};
library.json = {
  replacer: function(match, pIndent, pKey, pVal, pEnd) {
    var key = '<span class=json-key>';
    var val = '<span class=json-value>';
    var str = '<span class=json-string>';
    var r = pIndent || '';
    if (pKey)
       r = r + key + pKey.replace(/[": ]/g, '') + '</span>: ';
    if (pVal)
       r = r + (pVal[0] == '"' ? str : val) + pVal + '</span>';
    return r + (pEnd || '');
  },
  prettyPrint: function(obj) {
    var jsonLine = /^( *)("[\w]+": )?("[^"]*"|[\w.+-]*)?([,[{])?$/mg;
    return JSON.stringify(obj, null, 3)
       .replace(/&/g, '&amp;').replace(/\\"/g, '&quot;')
       .replace(/</g, '&lt;').replace(/>/g, '&gt;')
       .replace(jsonLine, library.json.replacer);
  }
};

$(document).ready(function () {
  case_tb(1, '#box', '#case-tb');
});

function tab_tb(obj) {
  var value = $(obj).attr("value");
  empty();
  case_tb(value, '#box', '#case-tb');
};

function empty() {
  $('#case-tb').html('');
  $('#box').html('')
};

function case_tb(category, box_id, tb_id) {
  var co = category;
  $.ajax({
    url: '/case/get',
    type: 'POST',
    data: JSON.stringify({page: 1,showData: 10,category: co}),
    contentType: "application/json; charset=utf-8",
    success: function(init_data) {
      $(box_id).pagination({
        totalData:init_data.total,
        jump:false,
        showData:10,
        coping:true,
        homePage: '首页',
        endPage: '末页',
        prevContent: '上页',
        nextContent: '下页',
        callback: function(api){
          $.ajax({
            url: '/case/get',
            type: 'POST',
            data: JSON.stringify({page: api.getCurrent(),showData: 10,category: co}),
            contentType: "application/json; charset=utf-8",
            success: function(data) {
              // $(tb_id).html('');
              if (data.total==0) {
                $(tb_id).html('')
                $('#info').html('暂无数据');
              } else {
                $(tb_id).html('')
                $('#info').html('');
                append_tb(data, tb_id);
              };
            }
          })
        }
      },function(api){
        if (init_data.total==0) {
          empty();
          $('#info').html('暂无数据');
        } else {
          $('#info').html('');
          append_tb(init_data, tb_id);
        };
      });
    }
  })
};

function append_tb(data, tb_id) {
  var tbody = document.getElementById(tb_id.substr(1));
  for (var i = 0; i < data.cases.length; i++) {
    var trow = getdatarow(data.cases[i]);
    tbody.appendChild(trow);
  }
};

function getdatarow(h){
  var row = document.createElement('tr'); //创建行
  var checkbox = '<input type="checkbox" name="case" value='+h.id+'>'
  var tdcheckbox = document.createElement('td');
  tdcheckbox.innerHTML = checkbox;
  tdcheckbox.setAttribute('class', 'text-center');
  row.appendChild(tdcheckbox);

  var id = document.createElement('td');
  id.innerHTML = h.id;
  id.setAttribute('class', 'text-center');
  row.appendChild(id);

  var name = document.createElement('td');
  name.innerHTML = h.name;
  row.appendChild(name);

  var desc = document.createElement('td');
  desc.innerHTML = h.desc;
  row.appendChild(desc);

  var setting_vule = '<span class="lnr lnr-eye" aria-hidden="true" data-toggle="modal" data-target="#show" id="btn-case-update" value='+h.id+' onclick="show_case(this)">&nbsp;</span><span class="lnr lnr-cog" aria-hidden="true" data-toggle="modal" data-target="#update" id="btn-case-show" value='+h.id+' onclick="update_case(this)">&nbsp;</span><span class="lnr lnr-trash" aria-hidden="true" id="btn-case-update" value='+h.id+' onclick="del_confirm(this)">&nbsp;</span>'
  var setting = document.createElement('td');
  setting.setAttribute('class', 'text-center');
  setting.innerHTML = setting_vule;
  row.appendChild(setting);

  return row;
};

$(document).ready(function() {
  $('#testsubmit').on('change', function(){
  $('#submit').click();
  console.log('formUpload to submit');
  });
});

$(function() {
  $('#submit').click(function() {
    // event.preventDefault();
    var form_data = new FormData($('#uploadform')[0]);
    $.ajax({
      type: 'POST',
      url: '/case/uploadajax',
      data: form_data,
      contentType: false,
      processData: false,
      dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
      // console.log(data);
      // console.log(textStatus);
      // console.log(jqXHR);
      // console.log('Success!');
      // $("#resultFilename").text(data['name']);
      // $("#resultFilesize").text(data['size']);
      alert('上传成功!\n文件名称：'+data['name']+'\n'+'文件大小：'+data['size']);
    }).fail(function(data){
      alert('error!');
    });
  });
});