$(document).ready(function() {
    if($("#map").length==0)
        return;
    var url=window.location.toString();
    url=url.split("/");
    var lobby_id=url[url.length-2];
    $.ajax({
        'url': '/game-ajax/'+lobby_id+'/territory/get-all',
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
                var x=0,xn=0,y=0,yn=0;
                var c=this["coordinates"].split(",");
                for(i=0;i<c.length;i+=2) {
                    x=x+parseInt(c[i]);
                    y=y+parseInt(c[i+1]);
                    xn=xn+1;
                    yn=yn+1;
                }
                centerx=parseInt(x/xn);
                centery=parseInt(y/yn);
                console.log(centerx+" "+centery);
                el=document.createElement("div");
                el.setAttribute("class","map-square");
                el.setAttribute("id","square-"+this["name"]);
                el.style.left=centerx+"px";
                el.style.top=centery+"px";
                $("#map-squares")[0].append(el);
            });
            updateGameInfo(response);
        }
    });
});

function mapMouseOver(e) {
    $("#map-hover-img")[0].src="/static/map/border-"+e.target.getAttribute("name")+".png";
}

function mapMouseOut(e) {
    $("#map-hover-img")[0].src="/static/map/map.png";
}

var mapX=0;
var mapY=0;
var windowW=0;
var windowH=0;
var mapW=2048;
var mapH=2048;
var moveByX=0;
var moveByY=0;
$(document).ready(function() {
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
});
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

function updateGameInfo(data) {
    $.each(data,function() {
        console.log(this.name);
    });
}