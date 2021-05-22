var pathname = window.location.pathname;
if(pathname == '/rollup/'){
var today = new Date().toISOString().split('T')[0];
var date = $("#datePicker").val();
$("#datePicker").val(today);
$.ajax({
	url: '/bodytable/',
	type: 'POST',
	dataType: 'html',
	data: {class: $("#class").val(), subject: $("#subject").val(), date_roll_up: $("#datePicker").val()},
})
.done(function(data) {
	$("#body_tables").html(data)
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
	url: '/bodytable/',
	type: 'POST',
	dataType: 'html',
	data: {class: $("#class").val(), subject: $("#subject").val(), date_roll_up: $("#datePicker").val()},
	})
	.done(function(data) {
		$("#body_tables").html(data)
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
	url: '/bodytable/',
	type: 'POST',
	dataType: 'html',
	data: {class: $("#class").val(), subject: $("#subject").val(), date_roll_up: $("#datePicker").val()},
	})
	.done(function(data) {
		$("#body_tables").html(data)
		console.log("success");
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
});
$('#uploadForm').submit(function(event) {
	event.preventDefault();
	$form = $(this)
	var post_url = $(this).attr("action");
    var formData = new FormData(this);
    $.ajax({
    	url: post_url,
    	type: 'POST',
    	dataType: 'html',
    	data: formData,
    	contentType: false,
        cache: false,
   		processData:false,
    })
    .done(function(data) {
    	if (post_url == '/bodytable/') {
    		$("#body_tables").html(data);
    		console.log("roll up");
    	}else{
    		console.log('edit roll up');
    	}
    	
    })
    .fail(function() {
    	console.log("error");
    })
    .always(function() {
    	console.log("complete");
    });
});
$('#btn_roll_up').click(function(){
	if($('#file-input').val() == ''){
		Swal.fire({
		  icon: 'error',
		  title: 'Oops...',
		  text: 'Không có ảnh nào được chọn!'
		})
	}else{
		// upload image and face detection
	   $('#uploadForm').attr('action', '/bodytable/');
	   let timerInterval
	   Swal.fire({
		  title: 'Đang nhận diện!',
		  html: 'Vui lòng chờ ...',
		  timer: 100000,
		  timerProgressBar: true,
		  onBeforeOpen: () => {
		    Swal.showLoading()
		  },
		  onClose: () => {
		    clearInterval(timerInterval)
		  }
		}).then((result) => {
			Swal.fire({
			  position: 'center',
			  icon: 'success',
			  title: 'Xong',
			  showConfirmButton: false,
			  timer: 1000
			})
			$('#file-input').val(null);
		})
	}
});

$("#datePicker").change(function(event) {
	$.ajax({
	url: '/bodytable/',
	type: 'POST',
	dataType: 'html',
	data: {class: $("#class").val(), subject: $("#subject").val(), date_roll_up: $("#datePicker").val()},
	})
	.done(function(data) {
		$("#body_tables").html(data)
		console.log("success");
	})
	.fail(function() {
		console.log("error");
	})
	.always(function() {
		console.log("complete");
	});
});
$("#btn-camera").click(function(event) {
	var url = "/video_feed?class="+$("#class").val()+ "&subject=" + $("#subject").val() +"&date_roll_up=" + $("#datePicker").val();
	var win = window.open(url,'_blank','height=900,width=800');
	var timer = setInterval(function() { 
    if(win.closed) {
        clearInterval(timer);
    		$.ajax({
			url: '/bodytable/',
			type: 'POST',
			dataType: 'html',
			data: {class: $("#class").val(), subject: $("#subject").val(), date_roll_up: $("#datePicker").val()},
			})
			.done(function(data) {
				$("#body_tables").html(data)
				console.log("success");
			})
			.fail(function() {
				console.log("error");
			})
			.always(function() {
				console.log("complete");
			});
		    }
			}, 1);
});
}
