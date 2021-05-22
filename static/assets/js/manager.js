var pathname = window.location.pathname;  
var url = window.location.href; 
if(pathname == '/manager/'){
	function deleteClass(id) {
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
	    	window.location.href = "/managerdelete?class=" + id;
	    }, 500);
		
	  }
	})
	}
	function deleteSubject(id) {
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
	    	window.location.href = "/managerdelete?subject=" + id;
	    }, 500);
		
	  }
	})
}
	
	function editClass(name, id) {
		$("#input-edit").val(name);
		$("#input-action").val('class');
		$("#input-id").val(id);
	}
	function editSubject(name, id) {
		$("#input-edit").val(name);
		$("#input-action").val('subject');
		$("#input-id").val(id);
	}
	$("#button-save-edit").click(function(event) {
		var name = $("#input-edit").val();
		var action = $("#input-action").val();
		var id = $("#input-id").val();
		window.location.href = "/manageredit?"+action+"="+ id+"&name="+name;
	});
}