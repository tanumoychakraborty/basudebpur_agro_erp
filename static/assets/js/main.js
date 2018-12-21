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
	
   $('#transaction_date').datetimepicker();
   
   $("#purchase-add-form").submit(function(e) {
	   
   		var purchase_lines = new Array();
   		$('#purchase_line_add_table tr').each(function(row, tr){
		    purchase_lines[row]={
		        "item" 				: $(tr).find('td:eq(1)').find('input').val(),
		        "itemDescription" 	:$(tr).find('td:eq(2)').find('input').val(),
		        "bookingUnitPrice" 	: $(tr).find('td:eq(4)').find('input').val(),
		        "bookingQuantity" 	: $(tr).find('td:eq(5)').find('input').val(),
		        "discount" 			: $(tr).find('td:eq(6)').find('input').val(),
		        "receiptUnitPrice" 	:$(tr).find('td:eq(7)').find('input').val(),
		        "receiptQuantity" 	: $(tr).find('td:eq(8)').find('input').val(),
		        "unitOfMeasure" 	: $(tr).find('td:eq(9)').find('input').val()
		    }
		}); 
   		var formData = {
            'weighting_number'    : $('input[id=weighting_number]').val(),
            'supplier'            : $('input[id=supplier]').val(),
            'transaction_date'    : $('input[id=transaction_date]').val(),
            'amount'    		  : $('input[id=amount]').val(),
            'buyer'            	  : $('input[id=buyer]').val(),
            'order_type'    	  : $('input[id=order_type]').val(),
            'vehicle_number'      : $('input[id=vehicle_number]').val(),
            'lines'				  : purchase_lines
        };
        
        $.ajax({
            type        : 'POST',
            url         : '/purchase/add/',
            data        : formData,
            dataType    : 'json',
            encode      : true
        }).done(function() {
                console.log('ok'); 
        });
        e.preventDefault();
        });
});
