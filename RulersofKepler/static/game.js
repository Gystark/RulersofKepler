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

var mapX=0;
var mapY=0;
var windowW=0;
var windowH=0;
var mapW=2048;
var mapH=2048;
var moveByX=0;
var moveByY=0;
window.addEventListener("load",function() {
	$("#map")[0].style.marginLeft="0px";
	$("#map")[0].style.marginTop="0px";
	$("#map")[0].style.width=mapW+"px";
	$("#map")[0].style.height=mapH+"px";
	$("#map")[0].addEventListener("mousedown",mapMouseDown,true);
	$("#map")[0].addEventListener("mousemove",mapMouseMove,true);
	$("#map")[0].addEventListener("mouseout",function() {moveByX=0; moveByY=0;},true);
	window.addEventListener("resize",windowResize,true);
	windowW=parseInt(window.getComputedStyle($("#map-holder")[0],null).getPropertyValue("width"));
	windowH=parseInt(window.getComputedStyle($("#map-holder")[0],null).getPropertyValue("height"));
	setTimeout("moveMapListener();",50);
},true);
function moveMapListener() {
	var x,y;
	x=parseInt($("#map")[0].style.marginLeft);
	y=parseInt($("#map")[0].style.marginTop);
	x+=moveByX;
	y+=moveByY;
	mapMove(x,y);
	setTimeout("moveMapListener();",50);
}
function mapMouseDown(event) {
	var tx,ty;
	tx=event.pageX-parseInt($("#map")[0].style.marginLeft);
    ty=event.pageY-35-parseInt($("#map")[0].style.marginTop);
	if(event.preventDefault) event.preventDefault();
	else event.returnValue=false;
	mapX=event.clientX;
	mapY=event.clientY;
	return false;
}
function mapMouseMove(event) {
	var x,y,mouseX,mouseY;
	x=parseInt($("#map")[0].style.marginLeft);
	y=parseInt($("#map")[0].style.marginTop);
	mouseX=event.clientX;
	mouseY=event.clientY;
	if(event.buttons==0) {
		if(mouseX<50) moveByX=15+(50-mouseX);
		else if (mouseX>windowW-50) moveByX=-15+(windowW-50-mouseX);
		else moveByX=0;
		
		if(mouseY<(50+35)) moveByY=15+(50+35-mouseY);
		else if(mouseY>windowH+35-50) moveByY=-15+(windowH+35-50-mouseY);
		else moveByY=0;
	}
	if(event.preventDefault) event.preventDefault();
	else event.returnValue=false;
	if(event.buttons!=1) {
		return false;
	}
	x+=(mouseX-mapX);
	y+=(mouseY-mapY);
	mapMove(x,y);
	mapX=mouseX;
	mapY=mouseY;
	return false;
}
function windowResize(event) {
	windowW=parseInt(window.getComputedStyle($("#map-holder")[0],null).getPropertyValue("width"));
	windowH=parseInt(window.getComputedStyle($("#map-holder")[0],null).getPropertyValue("height"));
	x=parseInt($("#map")[0].style.marginLeft);
	y=parseInt($("#map")[0].style.marginTop);
	mapMove(x,y);
}
function mapMove(x,y) {
    if(windowW>=mapW)
        x=0;
    else {
        if(x>0) x=0;
        else if(x<-mapW+windowW) x=-mapW+windowW;
    }
    if(windowH>=mapH)
        y=0;
    else {
        if(y>0) y=0;
        else if(y<-mapH+windowH) y=-mapH+windowH;
    }
	$("#map")[0].style.marginLeft=x+"px";
	$("#map")[0].style.marginTop=y+"px";
}