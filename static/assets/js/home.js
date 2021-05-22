var pathname = window.location.pathname;  
var url = window.location.href; 
if(pathname == '/'){
	function deleteStudent(id) {
		Swal.fire({
		  title: 'Bạn có chắc không?',
		  text: "Dữ liệu bị xoá sẽ không thể phục hồi",
		  icon: 'warning',
		  showCancelButton: true,
		  confirmButtonColor: '#3085d6',
		  cancelButtonColor: '#d33',
		  confirmButtonText: 'Yes, delete it!'
		}).then((result) => {
		  if (result.value) {
		    Swal.fire({
			  position: 'center',
			  icon: 'success',
			  title: 'Xoá thành công',
			  showConfirmButton: false,
			  timer: 1000
			})
		    setTimeout(function() {
		    	window.location.href = "/delete?id=" + id;
		    }, 500);
			
		  }
		})
	}
	if(url.search('success') > 0){
	  Swal.fire({
	  position: 'center',
	  icon: 'success',
	  title: 'Sửa thành công',
	  showConfirmButton: false,
	  timer: 1000
	})
	}
}