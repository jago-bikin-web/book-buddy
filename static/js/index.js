$(document).ready(() => {
    $(".button-nav-mobile").click(() => {
      $(".nav-mobile").removeClass("hidden")
    })

    $(".button-close-nav-mobile").click(() => {
      $(".nav-mobile").addClass("hidden")
    })  
  }
)