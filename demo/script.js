function $(div) {
	return document.getElementById(div);
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
	$("map").style.marginLeft="0px";
	$("map").style.marginTop="0px";
	$("map").style.width=mapW+"px";
	$("map").style.height=mapH+"px";
	$("map").addEventListener("mousedown",mapMouseDown,true);
	$("map").addEventListener("mousemove",mapMouseMove,true);
	$("map").addEventListener("mouseout",function() {moveByX=0; moveByY=0;},true);
	window.addEventListener("resize",windowResize,true);
	windowW=parseInt(window.getComputedStyle($("mapholder"),null).getPropertyValue("width"));
	windowH=parseInt(window.getComputedStyle($("mapholder"),null).getPropertyValue("height"));
	setTimeout("moveMapListener();",50);
},true);
function moveMapListener() {
	var x,y;
	x=parseInt($("map").style.marginLeft);
	y=parseInt($("map").style.marginTop);
	x+=moveByX;
	y+=moveByY;
	mapMove(x,y);
	setTimeout("moveMapListener();",50);
}
function mapMouseDown(event) {
	if(event.buttons!=1) {
		$("static").innerHTML="";
	}
	else {
		var tx,ty;
		tx=event.pageX-parseInt($("map").style.marginLeft);
		ty=event.pageY-71-parseInt($("map").style.marginTop);
	}
	if(event.preventDefault) event.preventDefault();
	else event.returnValue=false;
	mapX=event.clientX;
	mapY=event.clientY;
	return false;
}
function mapMouseMove(event) {
	var x,y,mouseX,mouseY;
	x=parseInt($("map").style.marginLeft);
	y=parseInt($("map").style.marginTop);
	mouseX=event.clientX;
	mouseY=event.clientY;
	if(event.buttons==0) {
		if(mouseX<50) moveByX=15+(50-mouseX);
		else if (mouseX>windowW-50) moveByX=-15+(windowW-50-mouseX);
		else moveByX=0;
		
		if(mouseY<(50+71)) moveByY=15+(121-mouseY);
		else if(mouseY>windowH+21) moveByY=-15+(windowH+21-mouseY);
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
	windowW=parseInt(window.getComputedStyle($("mapholder"),null).getPropertyValue("width"));
	windowH=parseInt(window.getComputedStyle($("mapholder"),null).getPropertyValue("height"));
	x=parseInt($("map").style.marginLeft);
	y=parseInt($("map").style.marginTop);
	mapMove(x,y);
}
function mapMove(x,y) {
	if(x>0) x=0;
	else if(x<-mapW+windowW) x=-mapW+windowW;
	if(y>0) y=0;
	else if(y<-mapH+windowH) y=-mapH+windowH;
	$("map").style.marginLeft=x+"px";
	$("map").style.marginTop=y+"px";
}