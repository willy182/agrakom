//Preloader
$(window).load(function () {
    "use strict";
   	$("#status").fadeOut();
	$("#preloader").delay(150).fadeOut("slow");
});
jQuery(document).ready(function($) {
	"use strict";
	//staller
	jQuery(window).stellar({horizontalScrolling:!1});
	
	//scroll top	
	$('.scrollup').click(function(){
		$("html, body").animate({ scrollTop: 0 }, 1000);
		return false;
	});
	
	// Smooth Scroll to internal links
    //$('.smooth-scroll').smoothScroll({
     //   offset: 30,
      //  speed: 1000
    //});
	
	// nav

  $('.singlepage').singlePageNav({
      filter: ':not(.external)',
	  currentClass: 'selected'
  });

  $('.scrolldown').singlePageNav({
      filter: ':not(.external)'
  });


	//fit video width
	jQuery('.fluid-width-video-wrapper').fitVids();
	jQuery('.fluid-width-video-wrapper').css('padding-top','56.25%'); // Always display videos 16:9 (100/16*9=56.25)
	
	//skill section
	$(".skillbar").each(function(){
		var e=$(this).attr("data-percent");
			$(this).waypoint(function(){
				$(this).find(".skillbar-bar").animate({width:e},2e3),
				$(this).find(".skill-bar-percent").animate({left:e,"margin-left":"-19px",opacity:1},2e3)
			},{offset:"90%",triggerOnce:!0})
		})
		
		$('.accordion').on('show', function (e) {
		
			$(e.target).prev('.accordion-heading').find('.accordion-toggle').addClass('active');
			$(e.target).prev('.accordion-heading').find('.accordion-toggle i').removeClass('icon-plus');
			$(e.target).prev('.accordion-heading').find('.accordion-toggle i').addClass('icon-minus');
		});
		
		$('.accordion').on('hide', function (e) {
			$(this).find('.accordion-toggle').not($(e.target)).removeClass('active');
			$(this).find('.accordion-toggle i').not($(e.target)).removeClass('icon-minus');
			$(this).find('.accordion-toggle i').not($(e.target)).addClass('icon-plus');
		});	

	//about block
	$(".n2").delay(500).queue(function(){$(this).addClass("roda")});
	
	//selected menu link
	$('#menu-main li a').click(function(){
		var links = $('#menu-main li a');
		links.removeClass('selected');
		$(this).addClass('selected');
	});
	
	//Animation
    var iOS = false,
        p = navigator.platform;
    if (p === 'iPad' || p === 'iPhone' || p === 'iPod') {
        iOS = true;
    }		
    if (iOS === false) {
        $('.flyIn').bind('inview', function (event, visible) {
            if (visible === true) {
                $(this).addClass('animated fadeInUp');
            }
        });
        $('.flyLeft').bind('inview', function (event, visible) {
            if (visible === true) {
                $(this).addClass('animated fadeInLeftBig');
            }
        });
        $('.flyRight').bind('inview', function (event, visible) {
            if (visible === true) {
                $(this).addClass('animated fadeInRightBig');
            }
        });
    }
	
	// add animation on hover
		$(".service-box").hover(
			function () {
			$(this).find('i').addClass("animated pulse");
			$(this).find('h2').addClass("animated fadeInUp");
			},
			function () {
			$(this).find('i').removeClass("animated pulse");
			$(this).find('h2').removeClass("animated fadeInUp");
			}
		);

	
	//counter
	$(".funfacts").waypoint(function(){$(".ch-info-front h1").countTo()},{offset:"90%",triggerOnce:!0})
	
	// portfolio
	var $container = $('#portfolio-wrap');
	$container.isotope({ itemSelector : '.portfolio-item'	});	
	$(window).resize(function() {
		$container.isotope('reLayout');
	});
	// filter items when filter link is clicked
	$('#filters a').click(function(){
		$('#filters a').removeClass('active');
		$(this).addClass('active');
		var selector = $(this).attr('data-filter');
		$container.isotope({ filter: selector });
		return false;
	});
	
	// flexslider main
	$('#main-flexslider').flexslider({						
		animation: "swing",
		direction: "vertical", 
		slideshow: true,
		slideshowSpeed: 3500,
		animationDuration: 1000,
		directionNav: false,
		prevText: '<i class="fa fa-angle-up icon-2x"></i>',       
		nextText: '<i class="fa fa-angle-down icon-2x active"></i>', 
		controlNav: false,
		smootheHeight:true,						
		useCSS: false
	});
	
		// client Carousel
	jQuery(".client-slider").owlCarousel({
		lazyLoad : true,
		slideSpeed : 300,
		stopOnHover: true,
		paginationSpeed : 400,
		autoPlay: 3500,
		navigation : false,
		pagination : false,
		autoHeight : true,
		items : 4, //10 items above 1000px browser width
		itemsDesktop : [1000,4], //5 items between 1000px and 901px
		itemsDesktopSmall : [900,3], // betweem 900px and 601px
		itemsTablet: [600,2], //2 items between 600 and 0
		itemsMobile : [420,1],
	});
	
		// testimonial Carousel
	jQuery(".testimonial-slider").owlCarousel({
		lazyLoad : true,
		slideSpeed : 300,
		stopOnHover: true,
		paginationSpeed : 400,
		autoPlay: 3500,
		navigation : true,
		pagination : false,
		autoHeight : true,
		navigationText : ["",""],
		items : 1, //10 items above 1000px browser width
		itemsDesktop : [1000,1], //5 items between 1000px and 901px
		itemsDesktopSmall : [900,1], // betweem 900px and 601px
		itemsTablet: [600,1], //2 items between 600 and 0
		itemsMobile : [420,1],
	});
	
	//project slider
	jQuery(".project-slider").owlCarousel({
		lazyLoad : true,
		slideSpeed : 300,
		stopOnHover: true,
		paginationSpeed : 400,
		autoPlay: 3500,
		navigation : true,
		pagination : false,
		autoHeight : true,
		navigationText : ["<i class='fas fa-chevron-circle-left'></i>","<i class='fas fa-chevron-circle-right'></i>"],
		items : 1, //10 items above 1000px browser width
		itemsDesktop : [1000,1], //5 items between 1000px and 901px
		itemsDesktopSmall : [900,1], // betweem 900px and 601px
		itemsTablet: [600,1], //2 items between 600 and 0
		itemsMobile : [420,1],
	});
	
	//Twitter feed
	jQuery(function(){
		jQuery('#tweet').tweetable({
		username: 'envato', //twitter username 
		time: true, 
		rotate: true, 
		speed: 7000, 
		limit: 5, 
		replies: true,
		position: 'append',
		failed: "Sorry, twitter is currently unavailable for this user.",
		loading: "Loading tweets...",
		html5: true,
		onComplete:function($ul){
			$('time').timeago();
		}
		});
	});

	/* Initialize GALLERY SLIDER */	
	var swiper = jQuery('#swiper').swiper({
		loop:true,
		grabCursor: true,
		autoPlay: 4000,
		keyboardControl:true
	});
	
	/* On Load swiper height should adjust to img size */
	jQuery('.swiper-slide img').load(function() {
		jQuery('#swiper').height(jQuery('.swiper-slide img').height());
		jQuery('.swiper-wrapper').height(jQuery('.swiper-slide img').height());
	});
	
	/* On Resize swiper height should adjust to img size */
	jQuery(window).resize(function() {
		jQuery('#swiper').height(jQuery('.swiper-slide img').height());
		jQuery('.swiper-wrapper').height(jQuery('.swiper-slide img').height());
	});
	

		// Google Maps
		// Creating a LatLng object containing the coordinate for the center of the map
		var posLatitude = $('#map').data('position-latitude'),
			posLongitude = $('#map').data('position-longitude'),
			latlng = new google.maps.LatLng(posLatitude,posLongitude);
		
		var mapstyles = [ { "stylers": [ { "invert_lightness": true }, { "weight": 0.1 }, { "hue": "#000000" }, { "visibility": "on" }, { "saturation": -100 }, { "lightness": 20 }, { "gamma": 1.2 } ] } ];

		// Creating an object literal containing the properties we want to pass to the map
		var options = {
			zoom: 16, // This number can be set to define the initial zoom level of the map
			center: latlng,
			mapTypeControlOptions: {  
				mapTypeIds: ['Styled']  
			},
			mapTypeId: 'Styled',
			mapTypeControl: false,
			scaleControl: false,
			streetViewControl: false,
			panControl: true,
			disableDefaultUI: true,
		};
		
		var map = new google.maps.Map(document.getElementById('map'), options),
			styledMapType = new google.maps.StyledMapType(mapstyles, { name: 'Styled' }),
			markerImage = $('#map').data('marker-img'),
			markerWidth = $('#map').data('marker-width'),
			markerHeight = $('#map').data('marker-height');
			
		map.mapTypes.set('Styled', styledMapType); 

		// Define Marker properties
		var image = new google.maps.MarkerImage(markerImage,
			// This marker is 64 pixels wide by 58 pixels tall.
			new google.maps.Size(markerWidth, markerHeight),
			new google.maps.Point(0,0),
			new google.maps.Point(18, 42)
		);

		// Add Marker
		var marker1 = new google.maps.Marker({
			position: latlng,
			map: map,
			icon: image
		});
});
