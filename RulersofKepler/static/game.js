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

$(document).ready(function() {
    if($("#map").length==0)
        return;
    $.ajax({
        'url': '/game-ajax/territory/get-all',
        'method': 'GET',
        success: function(data) {
            var response=$.parseJSON(JSON.stringify(data));
            $.each(response,function() {
                var el=document.createElement("area");
                el.setAttribute("shape","poly");
                el.setAttribute("coords",this["coordinates"]);
                el.setAttribute("name",this["name"]);
                el.addEventListener("mouseover",mapMouseOver,true);
                el.addEventListener("mouseout",mapMouseOut,true);
                $("#map-regions")[0].append(el);
            });
        }
    });
});

function mapMouseOver(e) {
    $("#map-hover-img")[0].src="/static/map/border-"+e.target.getAttribute("name")+".png";
}

function mapMouseOut(e) {
    $("#map-hover-img")[0].src="";
}