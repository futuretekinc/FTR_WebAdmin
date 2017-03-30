jQuery.each([ "put", "delete" ], function(i, method) {
	jQuery[method] = function(url, data, callback, type) {
		if (jQuery.isFunction(data)) {
			type = type || callback;
			callback = data;
			data = undefined;
		}

		return jQuery.ajax({
			url : url,
			type : method,
			dataType : type,
			data : data,
			success : callback
		});
	};
}); 

$.extend({
	postJSON : function(url, data, callback) {
		return $.post(url, data, callback, 'json');
	}
});

$.extend({
	openMenu : function(menu_id) {
		var mid = menu_id.substring(0,2);
		var $node = $('#'+menu_id);
		// init-menu
		$('#side-menu').find('*').removeClass('active in');
		
		if (mid == 'M1') {
			$node.addClass('active');
			$node.closest('ul').addClass('in');
			$node.closest('#ftr_menu').addClass('active');
		} else if (mid == 'M2') {
			$node.addClass('active');
			$node.closest('ul').addClass('in');
			$node.closest('#ftr_menu').addClass('active');
			$node.closest('ul').parent().addClass('active');
			$node.closest('ul').parent().closest('ul').addClass('in');
			$node.closest('ul').parent().closest('ul').parent().addClass('active');
		}		
	}
});

function fn_openMenu(menu_id) {
	var mid = menu_id.substring(0,2);
	var $node = $('#'+menu_id);
	// init-menu
	$('#side-menu').find('*').removeClass('active in');
	
	if (mid == 'M1') {
		$node.addClass('active');
		$node.closest('ul').addClass('in');
		$node.closest('#ftr_menu').addClass('active');
	} else if (mid == 'M2') {
		$node.addClass('active');
		$node.closest('ul').addClass('in');
		$node.closest('#ftr_menu').addClass('active');
		$node.closest('ul').parent().addClass('active');
		$node.closest('ul').parent().closest('ul').addClass('in');
		$node.closest('ul').parent().closest('ul').parent().addClass('active');
	}
}
