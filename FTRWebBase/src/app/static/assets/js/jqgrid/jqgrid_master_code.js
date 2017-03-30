function search_detail(master_code) {
	var filters = [{"name": "comm_code", "op": "equals", "val": master_code }];
	$.ajax({
		url: '/api/CM_CODED',
		data: {"q": JSON.stringify({"filters": filters})},
		dataType: "json",
		contentType: "application/json",
		success: function(data) { 
//        			$('#table_jqgrid_002').setGridParam({'data':data}).trigger("reloadGrid");
			var allParams = $('#table_jqgrid_002').jqGrid('getGridParam');
			allParams.data = data.objects;
			allParams.caption = "Master Code - " + master_code;
			$('#table_jqgrid_002').trigger('reloadGrid');
		}
	});
}


    function jqGrid_master_code() {
        
        
    	$(function(){
    		var JQ_TABLE_SERIAL_ID = '#table_jqgrid_001';
    		var JQ_TABLE_SERIAL_PAGE = '#table_jqgrid_001_page';
    		
    		function get_restless_url(page) {
    			var RPG = 5; // results_per_page
    			return "/api/CM_CODEM?results_per_page="+RPG+"&page="+page
    		}
    		
    		var SRV_EDIT_URL = '/cmm/jqgrid_handler';
    		var TBL_HEIGHT = 220;
    		var TBL_COLNAMES = [ '마스터코드' , '코드설명' , '보조1' , '보조2' , '보조3' , '보조4' ];
    		var TBL_COLMODEL = [
    			{name: 'comm_code', sortable:false, editable: true, index: 'comm_code', width: 100, align: 'center'},
    			{name: 'comm_cdnm', sortable:false, editable: true,  index: 'comm_cdnm', width: 100, align: 'center'},
    			{name: 're1f_desc', sortable:false, editable: true,  index: 're1f_desc', width: 100, align: 'center'},
    			{name: 're2f_desc', sortable:false, editable: true,  index: 're2f_desc', width: 100, align: 'center'},
    			{name: 're3f_desc', sortable:false, editable: true,  index: 're3f_desc', width: 100, align: 'center'},
    			{name: 're4f_desc', sortable:false, editable: true,  index: 're4f_desc', width: 100, align: 'center'},
    		];
    		
    		var jqGridOptions = {
    				url: get_restless_url(1),
    				datatype: "json",
    				ajaxGridOptions: { contentType: "application/json" },
//    				postData: "",
    				jsonReader: {
    					repeatitems: false,
    					page: "page",
    					total: "total_pages", 
    					records: "num_results",
    					root: function (obj) {
    						return obj.objects;
    					}
    				},
    				height: TBL_HEIGHT,
    				autowidth: true,
    				gridview:false,
    				shrinkToFit: true,
    				colNames: TBL_COLNAMES ,
    				colModel: TBL_COLMODEL ,
    				pager: JQ_TABLE_SERIAL_PAGE,
    				viewrecords: true,
    				editurl : SRV_EDIT_URL ,
    				add: true,
    				edit: true,
    				addtext: 'Add',
    				edittext: 'Edit',
    				hidegrid: false,
    			};
    			
    			
    			/** ---------------------------------------------------------------------- */
    			/* option - 테이블 캡션 달기 */
    			//jqGridOptions['caption'] = 'CM_CODED';
    			
    			////////////////////////////////////////////////////////////////////////
    			// EVENT 
    			////////////////////////////////////////////////////////////////////////

    			jqGridOptions['onPaging'] = function(action) {
    				   var _page = $(JQ_TABLE_SERIAL_ID).getGridParam("page");
    				   var total_id = '#sp_1_' + JQ_TABLE_SERIAL_PAGE.replace('#','');
    				   var total_pages = parseInt($(total_id).text());

    				   function reload_grid(p_page) {
    					   $(JQ_TABLE_SERIAL_ID).setGridParam({'page':p_page});
    					   $(JQ_TABLE_SERIAL_ID).setGridParam({url:get_restless_url(p_page)}).trigger("reloadGrid");
    				   }

    				if(action.indexOf('next_') >= 0) {
    					   if ((_page + 1) <= total_pages) {
    						   _page = _page + 1;
    						   reload_grid(_page);
    					   }
    				   } else if(action.indexOf('last_') >= 0) {
    					   reload_grid(total_pages);
    				   } else if(action.indexOf('prev_') >= 0) {
    					   if((_page - 1) >= 0) {
    						   _page = _page - 1;
    						   reload_grid(_page);
    					   }
    				   } else if(action.indexOf('first_') >= 0) {				    		
    					   reload_grid(1);
    				   }
    			}

    			jqGridOptions['onCellSelect'] = function(rowId,icol) {
    				var row = $(JQ_TABLE_SERIAL_ID).getRowData(rowId);
    				search_detail(row.comm_code);
    			}

    			// render jqgrid
    			$(JQ_TABLE_SERIAL_ID).jqGrid(jqGridOptions);
    			
    			/** ---------------------------------------------------------------------- */
    			$(JQ_TABLE_SERIAL_ID).jqGrid('navGrid', JQ_TABLE_SERIAL_PAGE,
    					{edit: true, add: true, del: true, search: true},
    					{height: 400, reloadAfterSubmit: true}
    			);
    			
    			$(JQ_TABLE_SERIAL_PAGE+'_right > div').hide();
    			
    			$(window).bind('resize', function () {
    				var width = $('.jqGrid_wrapper').width();
    			});
    			
    			 setTimeout(function(){
    				$('.wrapper-content').removeClass('animated fadeInRight');
    			 },700);
    		
    	});
    }