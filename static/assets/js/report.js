var pathname = window.location.pathname;  
var url = window.location.href; 
if(pathname == '/report/'){
	$("#btnExport").click(function(){
	  $("#table_report").table2excel({
	    // exclude CSS class
	    exclude: ".noExl",
	    name: "Điểm danh",
	    filename: "Điểm danh_" + $("#class").val() + "_" + $("#subject").val(), //do not include extension
	    fileext: ".xls", // file extension
	  }); 
	});

	$.ajax({
		url: '/bodyreport/',
		type: 'GET',
		dataType: 'html',
		data: {class: $("#class").val(), subject: $("#subject").val()},
	})
	.done(function(data) {
		$("#table_report").html(data)
		$("#button_show_absent").html((($("td").length + $("th").length)/$("tr").length)-3);
		console.log("success");
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});

	$("#class").change(function(){
		$.ajax({
		url: '/bodyreport/',
		type: 'GET',
		dataType: 'html',
		data: {class: $("#class").val(), subject: $("#subject").val()},
		})
		.done(function(data) {
			$("#table_report").html(data)
			$("#button_show_absent").html((($("td").length + $("th").length)/$("tr").length)-3);
			console.log("success");
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});
	$("#subject").change(function(){
		$.ajax({
		url: '/bodyreport/',
		type: 'GET',
		dataType: 'html',
		data: {class: $("#class").val(), subject: $("#subject").val()},
		})
		.done(function(data) {
			$("#table_report").html(data)
			$("#button_show_absent").html((($("td").length + $("th").length)/$("tr").length)-3);
			console.log("success");
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});
	});
}