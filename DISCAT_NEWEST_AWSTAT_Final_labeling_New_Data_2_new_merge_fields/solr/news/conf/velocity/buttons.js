function register_action_btn() {
  $( "#queryReset" ).click(function( event ) {
    event.preventDefault();
    var url = $("#constraints a:first-child").attr("href");
    if (typeof url !== 'undefined') {
      window.location.replace(url);
    }
  });

  $('#admin_download').click(function( event ) {
    event.preventDefault();
    var url = window.location.href.slice(0, window.location.href.length-1)+'&fl=*&wt=csv&rows=9999999';
    var win = window.open(url, '_blank');
    win.focus();
  });

  $('#adminDropdown').click(function(){
    if ($(this).next(".dropdown-menu").is(":hidden")) {
      var password = prompt("Please enter the password", "This is for Admin Only!");
      if (password === "1234") {
        $(this).next(".dropdown-menu").toggle();
      }
    } else {
      $(this).next(".dropdown-menu").toggle();
    }  
  });
}


$( document ).ready(function() {
  register_action_btn();
});
