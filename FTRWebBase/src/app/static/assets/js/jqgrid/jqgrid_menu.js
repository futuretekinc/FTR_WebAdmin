$(function(){

	 var menu = [
   	  { "id": 1, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "top", "pid": 0, "url": "#" },
   	  { "id": 2, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_1", "pid": 1, "url": "#" },
   	  { "id": 9, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_2", "pid": 1, "url": "#" },
   	  { "id": 10, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_2", "pid": 1, "url": "#" },
   	  { "id": 3, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_2", "pid": 2, "url": "#" },
   	  { "id": 7, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_2", "pid": 2, "url": "#" },
   	  { "id": 8, "lv1": "Y", "lv2": "N", "lv3": "N", "lv4": "N", "name": "c_2", "pid": 2, "url": "#" }
   ];
   
   var tree = _.groupBy(menu,'pid');
   
   $.each(tree,function(k,v) {
   	//console.log(k)
   	//console.log(v)
   	for(var i = 0; i < v.length ;  i++) {
   		var _blank = '[-]';
   		for (var j = 0; j < k; j++) {
   			_blank += ' = = ';
   		}
   		console.log(_blank + v[i]['name'] + parseInt(10+Math.random()*100));
   	}
   });
	
	var menu = [];
	
	function search_detail22(master_code) {
    	var filters = [{"name": "comm_code", "op": "equals", "val": master_code }];
    	$.ajax({
    		url: '/api/CM_CODED',
    		data: {"q": JSON.stringify({"filters": filters})},
    		dataType: "json",
    		contentType: "application/json",
    		success: function(data) { 
//    			$('#table_jqgrid_002').setGridParam({'data':data}).trigger("reloadGrid");
    			var allParams = $('#table_jqgrid_002').jqGrid('getGridParam');
    			allParams.data = data.objects;
    			allParams.caption = "Master Code - " + master_code;
    			$('#table_jqgrid_002').trigger('reloadGrid');
    		}
    	});
    }
	
});





