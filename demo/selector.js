function $(div) {
    return document.getElementById(div);
}
window.addEventListener("load",onwinload,true);
var el;
var svgns="http://www.w3.org/2000/svg";
var territories=["Arabia","BestKorea","Catalona","Cathay","Constantinopolis","Endia","Eucraine","Franz","Gerfew","Hungry","Lapland","Macarony","Mess-a-donia","Mess-o-potamia","Persia","Scotchland","ScottishIsland","Severoslavia","Thingystan"]
function onwinload(event) {
    el=document.createElementNS(svgns,"image");
    el.setAttribute("href","map/map.png");
    el.setAttribute("x","0");
    el.setAttribute("y","0");
    el.setAttribute("width","2048px");
    el.setAttribute("height","2048px");
    $("svg").appendChild(el);
    for(i=0;i<territories.length;i++) {
        el=document.createElementNS(svgns,"image");
        el.setAttribute("href","map/border-"+territories[i]+".png");
        el.setAttribute("x","0");
        el.setAttribute("y","0");
        el.setAttribute("width","2048px");
        el.setAttribute("height","2048px");
        $("svg").appendChild(el);
    }
    $("svg").addEventListener("mouseup",onsvgclick,false);
    $("svg").addEventListener("mousemove",onsvgmousemove,false);
    $("svg").addEventListener("contextmenu",function(event) {event.preventDefault(); event.stopPropagation();},false);
}
var drawbegin=false;
var drawfirst=null;
var linecoords="";
function onsvgclick(e) {
    if(e.button==2) {
        $("drawline").setAttribute("x2",drawfirst.getAttribute("x1"));
        $("drawline").setAttribute("y2",drawfirst.getAttribute("y1"));
        $("drawline").setAttribute("id","");
        drawbegin=false;
        e.preventDefault();
        e.stopPropagation();
        drawfirst=null;
        $("line").innerHTML=$("line").innerHTML+"<br />"+linecoords;
        linecoords="";
        return false;
    }
    var x=e.pageX;
    var y=e.pageY;
    if(!drawbegin) {
        el=document.createElementNS(svgns,"line");
        el.setAttribute("x1",x);
        el.setAttribute("y1",y);
        el.setAttribute("x2",x);
        el.setAttribute("y2",y);
        el.setAttribute("id","drawline");
        el.setAttribute("stroke","#000000");
        el.setAttribute("stroke-width","3");
        $("svg").appendChild(el);
        drawfirst=el;
        linecoords=x+","+y;
        drawbegin=true;
    }
    else {
        $("drawline").setAttribute("id","");
        el=document.createElementNS(svgns,"line");
        el.setAttribute("x1",x);
        el.setAttribute("y1",y);
        el.setAttribute("x2",x);
        el.setAttribute("y2",y);
        el.setAttribute("id","drawline");
        el.setAttribute("stroke","#000000");
        el.setAttribute("stroke-width","3");
        $("svg").appendChild(el);
        linecoords=linecoords+","+x+","+y;
    }
}
function onsvgmousemove(e) {
    if(!drawbegin)
        return;
    var x=e.pageX;
    var y=e.pageY;
    $("drawline").setAttribute("x2",x);
    $("drawline").setAttribute("y2",y);
}