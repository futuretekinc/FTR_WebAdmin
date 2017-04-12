

function ftr_alert_confirm_normal(p_msg, p_callback) {
	bootbox.confirm({
	    message: p_msg,
	    buttons: {
	        confirm: { label: '<i class="fa fa-check"></i> 네', className: 'btn-primary' },
	        cancel: { label: '<i class="fa fa-times"></i> 아니오', className: 'btn-default' }
	    },
	    callback: p_callback
	});	
}

function ftr_swl_confirm() {
	
swal({
    title: "Are you sure?",
    text: "You will not be able to recover this imaginary file!",
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#DD6B55",
    confirmButtonText: "Yes, delete it!",
    closeOnConfirm: false
}, function () {
    swal("Deleted!", "Your imaginary file has been deleted.", "success");
});

}

function ftr_bootbox_confirm(msg,_callback) {
	bootbox.confirm({
	    message: msg,
	    buttons: {
	        confirm: {
	            label: '<i class="fa fa-check"></i> 네',
	            className: 'btn-success'
	        },
	        cancel: {
	            label: '<i class="fa fa-times"></i> 아니오',
	            className: 'btn-danger'
	        }
	    },
	    callback: _callback
	});
}