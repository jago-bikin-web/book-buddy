$(document).ready(() => {
  $(".button-nav-mobile").click(() => {
    $(".nav-mobile").removeClass("hidden");
  });

  $(".button-close-nav-mobile").click(() => {
    $(".nav-mobile").addClass("hidden");
  });
  
  $(".profile-picture").hover(() => {
    $(".profile-box").removeClass("hidden");
  } , () => {
    setTimeout(() => {
      $(".profile-box").addClass("hidden");
    }, 3200)
  })
  
  $(".profile-picture").click(() => {
    if ($(".profile-box").hasClass("hidden")) {
      $(".profile-box").removeClass("hidden");
    } else {
      $(".profile-box").addClass("hidden");
    }
  });
});
