"use strict";

$(document).ready(function () {
  // $(".main__content__container").focus()
  // const target = $('.main__content__container').offset().top;
  // window.scrollTo({
  //     top: target,
  //     behavior: 'instant'
  // });
  console.log('starting function');
  $('.main__slider').slick({
    //slide: 'div',
    slidesToShow: 1,
    dots: true,
    infinite: true,
    cssEase: 'ease',
    swipe: true,
    arrows: true,
    autoplay: true,
    autoplayspeed: 1000,
    centerMode: true,
    centerPadding: '60px' //  lazyLoad: 'ondemand',
    // rtl: true,
    // fade: true,

  });
  $('.product__slider').slick({
    //slide: 'div',
    slidesToScroll: 4,
    slidesToShow: 4,
    //dots: true,
    infinite: true,
    cssEase: 'ease',
    swipe: true,
    arrows: true,
    autoplay: true,
    autoplayspeed: 1000,
    // centerMode: true,
    //centerPadding: '60px',
    // lazyLoad: 'ondemand',
    // rtl: true,
    // fade: true,
    responsive: [{
      breakpoint: 991,
      settings: {
        slidesToScroll: 3,
        slidesToShow: 3
      }
    }, {
      breakpoint: 590,
      settings: {
        slidesToScroll: 2,
        slidesToShow: 2
      }
    }, {
      breakpoint: 423,
      settings: {
        slidesToScroll: 1,
        slidesToShow: 1
      }
    }]
  });
});
$(".mobile__menu__trigger").click(function () {
  $(".mobile__wrapper").addClass("show");
  $(".mobile__main").addClass("show");
  $("body").addClass("overflow");
});
$(".mobile__wrapper").click(function () {
  $(".mobile__wrapper").removeClass("show");
  $(".mobile__main").removeClass("show");
  $("body").removeClass("overflow");
});
$(".footer__feedback__button").click(function () {
  $(".contact__back").addClass("show");
  $(".contact__container").addClass("show");
});
$(".contact__back").click(function () {
  $(".contact__back").removeClass("show");
  $(".contact__container").removeClass("show");
});
$(".contact__close").click(function () {
  $(".contact__back").removeClass("show");
  $(".contact__container").removeClass("show");
});
$(".filter__block__heading").click(function () {
  var target = $(this).data("target");

  if ($(this).hasClass("show")) {
    $(this).removeClass("show");
    $(target).removeClass("show");
  } else {
    $(this).addClass("show");
    $(target).addClass("show");
  }
});
$(".mobile__filter__back").click(function () {
  console.log("clicked to close");
  $("body").removeClass("overflow");
  $(".filter__wrap").removeClass("show");
  $(this).removeClass("show");
});
$("#mobile__filter__button").click(function () {
  $("body").addClass("overflow");
  $(".filter__wrap").addClass("show");
  $(".mobile__filter__back").addClass("show");
});
$(".ck__container__btn").click(function () {
  console.log('clicked');
  $(".ck__wrap").addClass("hide");
});