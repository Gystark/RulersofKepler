$(document).ready(function () {
   $('#testButton').click(function () {

       var game = $(this).text().split('///');

       $.ajax({
          'url': '/game-ajax/' + game[0] + '/territory/' + game[1] + '/data/',
           'method': 'GET',
           success: function (data) {

              console.log(data);

               var response = $.parseJSON(JSON.stringify(data));

               $('#testid').text(response.owner);
           }
       });
   });
});