$(document).ready(function () {
  $(".one-post").hover(
    function (event) {
      $(event.currentTarget)
        .find(".one-post-shadow")
        .animate({ opacity: "0.1" }, 300);
    },
    function (event) {
      $(event.currentTarget)
        .find(".one-post-shadow")
        .animate({ opacity: "0" }, 300);
    },

    $(".logo").hover(
      function (event) {
        $(event.currentTarget).animate({ width: 320, height: 160.5 }, 300);
      },
      function (event) {
        $(event.currentTarget).animate({ width: 300, height: 150 }, 300);
      }
    )
  );
});
