$(document).ready(function () {
  var yPosition;
  var scrolled = 0;
  var $parallaxElements = $(".icons-for-parallax img");
  $(window).scroll(function () {
    scrolled = $(window).scrollTop();
    for (var i = 0; i < $parallaxElements.length; i++) {
      yPosition = scrolled * 0.15 * (i + 1);
      $parallaxElements.eq(i).css({ top: yPosition });
    }
  });

  var yPositionLogo;
  var scrolledLogo = 30;
  var $parallaxLogo = $(".logo");
  $(window).scroll(function () {
    scrolledLogo = $(window).scrollTop();
    yPositionLogo = scrolledLogo * 0.95;
    $parallaxLogo.css({ top: yPositionLogo });
  });
});
