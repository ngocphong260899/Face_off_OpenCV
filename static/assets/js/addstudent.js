var pathname = window.location.pathname;
var url = window.location.href;  
if(pathname == '/add/'){
	//click btn aadd student
	$('#btn-add-student').click(function(event) {
	 	if($('#file-input').val() !=''){
 		   Swal.fire({
			  title: 'Đang thêm khuôn mặt!',
			  html: 'Vui lòng chờ...',
			  timer: 100000,
			  timerProgressBar: true,
			  onBeforeOpen: () => {
			    Swal.showLoading()
			  },
			  onClose: () => {
			    clearInterval(timerInterval)
			  }
			}).then((result) => {
			})
	 	}
	});
	$('#btn-edit-student').click(function(event) {
	   Swal.fire({
	  title: 'Đang cập nhập dữ liệu!',
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
	})
});
	if(url.search('success') > 0){
	  Swal.fire({
	  position: 'center',
	  icon: 'success',
	  title: 'Thêm thành công',
	  showConfirmButton: false,
	  timer: 1000
	})
	}

}