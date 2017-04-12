function render_datatable(table_id, url, columns) {
	$(table_id).DataTable({
		'processing' : true 
		, 'bLengthChange' : false
		, 'destroy' : true 
		, 'ajax' : {
			'url' : url ,
			'type' : 'POST' ,
		}
		, 'columns' : columns
		, 'columnDefs' : [ {'className' : 'text-center', 'targets' : 'all'} ]
	});    	
}

function render_datatable_no_search(table_id, url, columns) {
	$(table_id).DataTable({
		'processing' : true 
		, 'bLengthChange' : false
		, 'destroy' : true 
		/* hide searhbar */
		, 'bFilter' : false
		, 'bInfo' : false
		/* hide searhbar */
		, 'ajax' : {
			'url' : url ,
			'type' : 'POST' ,
		}
		, 'columns' : columns
		, 'columnDefs' : [ {'className' : 'text-center', 'targets' : 'all'} ]
	});    	
}

function show_resource_table() {
	var target_name = 'resources'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ;
	var columns = [
		{'data' : 'res_id'} ,
		{'data' : 'res_name'} ,
	];
	render_datatable(table_id, url, columns);
}

function show_gateway_table() {
	var target_name = 'gateway'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ;
	var columns = [
		{'data' : 'gw_id'} ,
		{'data' : 'gw_name'} ,
	];
	render_datatable(table_id, url, columns);
}

function show_device_table() {
	var target_name = 'devices'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ; 
	var columns = [
		{'data' : 'dev_id'} ,
		{'data' : 'dev_name'} ,
		{'data' : 'dev_type'} ,
		{'data' : 'dev_info'} ,
		{'data' : 'dev_inst'} ,
		{'data' : 'delete'} ,
	];
	render_datatable_no_search(table_id, url, columns);
}

function show_endpoint_table() {
	var target_name = 'endpoints'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ; 
	var columns = [
		{'data' : 'ep_id'} ,
		{'data' : 'dev_id'} ,
		{'data' : 'ep_name'} ,
		{'data' : 'ep_scale'} ,
		{'data' : 'ep_unit'} ,
		{'data' : 'ep_pr_host'} ,
		{'data' : 'ep_interval'} ,
		{'data' : 'ep_limit'} ,
		{'data' : 'ep_hour'} ,
		{'data' : 'ep_day'} ,
		{'data' : 'ep_month'} ,
		{'data' : 'ep_count'} ,
	];
	render_datatable(table_id, url, columns);   	
} 


function show_eptype_table() {
	var target_name = 'eptype'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ;
	var columns = [
		{'data' : 'ep_type'} ,
		{'data' : 'ep_name'} ,
		{'data' : 'ep_scale'} ,
		{'data' : 'ep_unit'} ,
		{'data' : 'ep_pr_host'} ,
		{'data' : 'ep_interval'} ,
		{'data' : 'ep_limit'} ,
		{'data' : 'ep_hour'} ,
		{'data' : 'ep_day'} ,
		{'data' : 'ep_month'} ,
		{'data' : 'ep_count'} ,
		{'data' : 'delete'} ,
	];
//	console.log(table_id)
	render_datatable(table_id, url, columns);   	
}

function show_eptype_table_readonly() {
	var target_name = 'eptype'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ;
	var columns = [
		{'data' : 'ep_type'} ,
		{'data' : 'ep_name'} ,
		{'data' : 'ep_scale'} ,
		{'data' : 'ep_unit'} ,
		{'data' : 'ep_pr_host'} ,
		{'data' : 'ep_interval'} ,
		{'data' : 'ep_limit'} ,
		{'data' : 'ep_hour'} ,
		{'data' : 'ep_day'} ,
		{'data' : 'ep_month'} ,
		{'data' : 'ep_count'} , 
	];
//	console.log(table_id)
	render_datatable(table_id, url, columns);   	
}
 

 
function show_dvtype_table() {
	var target_name = 'devtype'
	var table_id = '.dataTables-'+target_name;
	var url = '/obm/' + target_name ;
	var columns = [
		{'data' : 'dv_type'} ,
		{'data' : 'dv_name'} ,
		{'data' : 'dv_location'} ,
		{'data' : 'dv_timeout'} ,
		{'data' : 'dv_protocol'} ,
		{'data' : 'dv_delete' }
	];
//	console.log(table_id)
	render_datatable(table_id, url, columns);   	
}



