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
	var host = "http://35.244.52.236:80"
   
   $("#purchase-add-form").submit(function(e) {
	   
   		var purchase_lines = new Array();
   		$('#purchase_line_add_table tr').each(function(row, tr){
		    purchase_lines[row-1]={
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        item_description 	: $(tr).find('td:eq(2)').find('input').val(),
		        line_status		 	: $(tr).find('td:eq(3)').find('option:selected').val(),
		        booking_unit_price 	: $(tr).find('td:eq(4)').find('input').val(),
		        booking_quantity 	: $(tr).find('td:eq(5)').find('input').val(),
		        discount 			: $(tr).find('td:eq(6)').find('input').val(),
		        receipt_unit_price 	: $(tr).find('td:eq(7)').find('input').val(),
		        receipt_quantity 	: $(tr).find('td:eq(8)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(9)').find('option:selected').val()
		    }
		}); 
   		var formData = {
            weighting_number    : $('input[id=weighting_number]').val(),
            supplier_id         : $('#supplier option:selected').val(),
            transaction_date    : $('input[id=transaction_date]').val(),
            amount    		  	: $('input[id=amount]').val(),
            buyer_id          	: $('p[id=buyer]').text(),
            order_type    	  	: $('#order_type option:selected').val(),
            vehicle_number      : $('input[id=vehicle_number]').val(),
            purchase_trx_number : $('input[id=purchase_trx_number]').val(),
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
		    	created_by			: $(tr).find('td:eq(0)').find('strong').attr('name'),
		    	line_number		 	: $(tr).find('td:eq(0)').find('strong').text(),
		        item_id 			: $(tr).find('td:eq(1)').find('option:selected').val(),
		        item_description 	: $(tr).find('td:eq(2)').find('input').val(),
		        line_status		 	: $(tr).find('td:eq(3)').find('option:selected').val(),
		        booking_unit_price 	: $(tr).find('td:eq(4)').find('input').val(),
		        booking_quantity 	: $(tr).find('td:eq(5)').find('input').val(),
		        discount 			: $(tr).find('td:eq(6)').find('input').val(),
		        receipt_unit_price 	: $(tr).find('td:eq(7)').find('input').val(),
		        receipt_quantity 	: $(tr).find('td:eq(8)').find('input').val(),
		        unit_of_measure		: $(tr).find('td:eq(9)').find('option:selected').val()
		    }
		}); 
   		var formData = {
   			purchase_trx_number : $('p[id=transaction_number]').text(),
   			weighting_number    : $('input[id=weighting_number]').val(),
            order_status  		: $('#header_status option:selected').val(),
            supplier_id         : $('#supplier option:selected').val(),
            transaction_date    : $('input[id=transaction_date]').val(),
            amount    		  	: $('input[id=amount]').val(),
            buyer_id            : $('input[id=buyer]').val(),
            order_type    	  	: $('#order_type option:selected').val(),
            vehicle_number      : $('input[id=vehicle_number]').val(),
            created_by			: $('input[id=buyer]').val(),
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
            effective_to         	: $('input[name=effective_to]').val(),
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
            effective_to         	: $('input[name=effective_to]').val(),
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
            			  }
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
    });
    
});
