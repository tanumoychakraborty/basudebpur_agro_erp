$.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;


	

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);


	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


	 
	 
	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		} 
			 
	}); 

	 
	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});


	// Load Resize 
	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
	});
			
	// Customizations
	var host = "http://localhost:8000"
   
   $("#purchase-add-form").submit(function(e) {
	   
   		var purchase_lines = new Array();
   		$('#purchase_line_add_table tr').each(function(row, tr){
		    purchase_lines[row-1]={
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        booking_unit_price 	: $(tr).find('td:eq(2)').find('input').val(),
		        booking_quantity 	: $(tr).find('td:eq(3)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(4)').find('option:selected').val()
		    }
		}); 
   		var formData = {
            supplier_id         : $('#supplier option:selected').val(),
            transaction_date    : $('input[id=transaction_date]').val(),
            buyer_id          	: $('p[id=buyer]').text(),
            purchase_trx_lines	: purchase_lines
        };
        
        $.ajax({
            type        : 'POST',
            url         : '/purchase/add/',
            data        : JSON.stringify(formData),
            dataType    : 'json',
            encode      : true,
            success		: function(data){
            				location.href = host+"/purchase/";
            			  },
            error		: function(jqXHR, exception){
            				if(jqXHR.status == 422){
                 	 		var card = document.getElementById('card-header');
           					var htmlcode = '';
           					Object.keys(jqXHR.responseJSON).forEach(function(key){
           						var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
           						var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
           						 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
           						 				text+
           						 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
           						 '                                               <span aria-hidden="true">X</span>  '  + 
           						 '                                           </button>  '  + 
           						 '                                      </div>  ' ; 
           						htmlcode += htmlcd;
           		    			});
           					htmlcode += card.innerHTML;
           					card.innerHTML = htmlcode;
           		    		}
           		    	}
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
    });
    
    $("#purchase-update-form").submit(function(e) {
	   
   		var purchase_lines = new Array();
   		$('#purchase_line_update_table tr').each(function(row, tr){
		    purchase_lines[row-1]={
		    	transaction_line_id : $(tr).find('td:eq(0)').find('strong').attr('value'),
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        booking_unit_price 	: $(tr).find('td:eq(2)').find('input').val(),
		        booking_quantity 	: $(tr).find('td:eq(3)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(4)').find('option:selected').val()
		    }
		}); 
   		var formData = {
   			purchase_trx_number : $('#transaction_number').text(),
            order_status  		: $('#header_status option:selected').val(),
            supplier_id         : $('#supplier option:selected').val(),
            transaction_date    : $('input[id=transaction_date]').val(),
            buyer_id            : $('input[id=buyer]').attr('name'),
            purchase_trx_lines	: purchase_lines
        };
        
        $.ajax({
            type        : 'PUT',
            url         : '/purchase/update/',
            data        : JSON.stringify(formData),
            dataType    : 'json',
            encode      : true,
            success		: function(data){
            				location.href = host+"/purchase/";
            			  },
            error		: function(jqXHR, exception){
            				if(jqXHR.status == 422){
                 	 		var card = document.getElementById('card-header');
           					var htmlcode = '';
           					Object.keys(jqXHR.responseJSON).forEach(function(key){
           						var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
           						var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
           						 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
           						 				text+
           						 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
           						 '                                               <span aria-hidden="true">X</span>  '  + 
           						 '                                           </button>  '  + 
           						 '                                      </div>  ' ; 
           						htmlcode += htmlcd;
           		    			});
           					htmlcode += card.innerHTML;
       		    			card.innerHTML = htmlcode;
            				}
           		    	}
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
    });
    
    
    $("#supplier-add-form").submit(function(e) {
	   
   		var supplier_lines = new Array();
   		$('#supplier_site_add_table tr').each(function(row, tr){
		    supplier_lines[row-1]={
		        supplier_site_code 		: $(tr).find('td:eq(1)').find('input').val(),
		        supplier_site_address 	: $(tr).find('td:eq(2)').find('input').val(),
		        phone_number1		 	: $(tr).find('td:eq(3)').find('input').val(),
		        phone_number2		 	: $(tr).find('td:eq(4)').find('input').val(),
		        email				 	: $(tr).find('td:eq(5)').find('input').val(),
		        inactive_date 			: $(tr).find('td:eq(6)').find('input').val()
		    }
		}); 
   		var formData = {
            supplier_code	    	: $('input[id=supplier_code]').val(),
            supplier_name         	: $('input[id=supplier_name]').val(),
            supplier_type		    : $('#supplier_type option:selected').val(),
            description    		  	: $('input[id=description]').val(),
            effective_from         	: $('input[id=effective_from]').val(),
            enabled_flag    	  	: $('#enabled').is(':checked'),
            remarks			        : $('input[id=remarks]').val(),
            effective_to         	: $('input[id=effective_to]').val(),
            supplier_master_sites	: supplier_lines
        };
        
        $.ajax({
            type        : 'POST',
            url         : '/supplier/add/',
            data        : JSON.stringify(formData),
            dataType    : 'json',
            encode      : true,
            success		: function(data){
            				location.href = host+"/supplier/";
            			  },
            error		: function(jqXHR, exception){
             	 			if(jqXHR.status == 422){
             	 				var card = document.getElementById('card-header');
       							var htmlcode = '';
       							Object.keys(jqXHR.responseJSON).forEach(function(key){
       								var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
       								var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
       								 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
       								 				text+
       								 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
       								 '                                               <span aria-hidden="true">X</span>  '  + 
       								 '                                           </button>  '  + 
       								 '                                      </div>  ' ; 
       								htmlcode += htmlcd;
       		    					});
       							htmlcode += card.innerHTML;
       		    				card.innerHTML = htmlcode;
       		    			}
       		    		}
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
    });
    
    $("#supplier-update-form").submit(function(e) {
	   
   		var supplier_lines = new Array();
   		$('#supplier_site_update_table tr').each(function(row, tr){
		    supplier_lines[row-1]={
		    	supplier_site_id		: $(tr).find('td:eq(0)').find('input').attr('name'),
		        supplier_site_code 		: $(tr).find('td:eq(0)').find('input').val(),
		        supplier_site_address 	: $(tr).find('td:eq(1)').find('input').val(),
		        phone_number1		 	: $(tr).find('td:eq(2)').find('input').val(),
		        phone_number2		 	: $(tr).find('td:eq(3)').find('input').val(),
		        email				 	: $(tr).find('td:eq(4)').find('input').val(),
		        inactive_date 			: $(tr).find('td:eq(5)').find('input').val()
		    }
		}); 
   		var formData = {
   			supplier_id				: $('input[id=supplier_code]').attr('name'),
            supplier_code	    	: $('input[id=supplier_code]').val(),
            supplier_name         	: $('input[id=supplier_name]').val(),
            supplier_type		    : $('#supplier_type option:selected').val(),
            description    		  	: $('input[id=description]').val(),
            effective_from         	: $('input[id=effective_from]').val(),
            enabled_flag    	  	: $('#enabled').is(':checked'),
            remarks			        : $('input[id=remarks]').val(),
            effective_to         	: $('input[id=effective_to]').val(),
            supplier_master_sites	: supplier_lines
        };
        
        $.ajax({
            type        : 'PUT',
            url         : '/supplier/update/',
            data        : JSON.stringify(formData),
            dataType    : 'json',
            encode      : true,
            success		: function(data){
            				location.href = host+"/supplier/";
            			  },
             error		: function(jqXHR, exception){
            	 			if(jqXHR.status == 422){
            	 				var card = document.getElementById('card-header');
  		    					var htmlcode = '';
  		    					Object.keys(jqXHR.responseJSON).forEach(function(key){
  		    						var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
  		    						var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
  		    						 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
  		    						 				text+
  		    						 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
  		    						 '                                               <span aria-hidden="true">X</span>  '  + 
  		    						 '                                           </button>  '  + 
  		    						 '                                      </div>  ' ; 
  		    						htmlcode += htmlcd;
  		    					});
  		    					htmlcode += card.innerHTML;
  		    					card.innerHTML = htmlcode;
  		    				}
  		    			}
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
    });
    
    
	$("#purchase-receipt-add-form").submit(function(e) {
	   
		var purchase_receipt_lines = new Array();
		var trx_number = $('strong[id=purchase_receipt]').attr('name');
		$('#purchase_receipt_line_add_table tr').each(function(row, tr){
			purchase_receipt_lines[row-1]={
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        weighing_number	: $(tr).find('td:eq(2)').find('input').val(),
		        load_unload_area 	: $(tr).find('td:eq(3)').find('input').val(),
		        quantity 			: $(tr).find('td:eq(4)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(5)').find('option:selected').val(),
		        unit_price 			: $(tr).find('td:eq(6)').find('input').val(),
		        discount 			: $(tr).find('td:eq(7)').find('input').val(),
		        receipt_line_status	: $(tr).find('td:eq(8)').find('option:selected').val()
		    }
		}); 
		var formData = {
			vehicle_number         	: $('input[id=truck_numer]').val(),
			receipt_date		    : $('input[id=purchase_receipt_date]').val(),
			challan_number     		: $('p[id=chalan_number]').text(),
			bata		     		: $('p[id=bata]').text(),
	        receipt_lines			: purchase_receipt_lines
	    };
    
	    $.ajax({
	        type        : 'POST',
	        url         : '/purchase/'+trx_number+'/add_receipt/',
	        data        : JSON.stringify(formData),
	        dataType    : 'json',
	        encode      : true,
	        success		: function(data){
	        				location.href = host+'/purchase/'+trx_number+'/';
	        			  },
	        error		: function(jqXHR, exception){
	        				if(jqXHR.status == 422){
		    					var card = document.getElementById('card-header');
		    					var htmlcode = '';
		    					Object.keys(jqXHR.responseJSON).forEach(function(key){
		    						var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
		    						var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
		    						 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
		    						 				text+
		    						 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
		    						 '                                               <span aria-hidden="true">X</span>  '  + 
		    						 '                                           </button>  '  + 
		    						 '                                      </div>  ' ; 
		    						htmlcode += htmlcd;
		    					});
		    					htmlcode += card.innerHTML;
		    					card.innerHTML = htmlcode;
		    				}
		    			}
	    }).done(function() {
	            console.log('ok'); 
	    });
	    e.preventDefault();
	});
	
	$("#purchase-receipt-update-form").submit(function(e) {
		   
		var purchase_receipt_lines = new Array();
		var trx_number = $('strong[id=purchase_receipt]').attr('name');
		var challan_number = $('p[id=chalan_number]').text();
		$('#purchase_receipt_line_add_table tr').each(function(row, tr){
			purchase_receipt_lines[row-1]={
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		    	receipt_line_id	 	: $(tr).find('td:eq(0)').find('strong').attr('value'),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        weighing_number		: $(tr).find('td:eq(2)').find('input').val(),
		        load_unload_area 	: $(tr).find('td:eq(3)').find('input').val(),
		        quantity 			: $(tr).find('td:eq(4)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(5)').find('option:selected').val(),
		        unit_price 			: $(tr).find('td:eq(6)').find('input').val(),
		        discount 			: $(tr).find('td:eq(7)').find('input').val(),
		        receipt_line_status	: $(tr).find('td:eq(8)').find('option:selected').val()
		    }
		}); 
		var formData = {
			vehicle_number         	: $('input[id=truck_numer]').val(),
			challan_date		    : $('input[id=challan_date]').val(),
			bata		     		: $('p[id=bata]').text(),
			challan_number     		: challan_number,
	        receipt_lines			: purchase_receipt_lines
	    };
    
	    $.ajax({
	        type        : 'PUT',
	        url         : '/purchase/'+trx_number+'/update_receipt/'+challan_number+'/',
	        data        : JSON.stringify(formData),
	        dataType    : 'json',
	        encode      : true,
	        success		: function(data){
	        				location.href = host+'/purchase/'+trx_number+'/';
	        			  },
	    	error		: function(jqXHR, exception){
	    					if(jqXHR.status == 422){
	    						var card = document.getElementById('card-header');
	    						var htmlcode = '';
	    						Object.keys(jqXHR.responseJSON).forEach(function(key){
	    							var text = key + '&nbsp:&nbsp' + jqXHR.responseJSON[key]
	    							var htmlcd =  '   <div class="sufee-alert alert with-close alert-danger alert-dismissible fade show">  '  + 
	    							 '                                           <span class="badge badge-pill badge-danger">Error</span>  '  + 
	    							 				text+
	    							 '                                           <button type="button" class="close" data-dismiss="alert" aria-label="Close">  '  + 
	    							 '                                               <span aria-hidden="true">X</span>  '  + 
	    							 '                                           </button>  '  + 
	    							 '                                      </div>  ' ; 
	    							htmlcode += htmlcd;
	    						});
	    						htmlcode += card.innerHTML;
	    						card.innerHTML = htmlcode;
	    					}
	    				}
	    }).done(function() {
	        console.log('ok'); 
	    });
	    e.preventDefault();
	});
});
