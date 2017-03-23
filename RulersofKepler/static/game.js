var territory_information = {};
var territory_neighbours = {};
$(document).ready(function () {
    if ($("#map").length == 0)
        return;
    var url = window.location.toString();
    url = url.split("/");
    var lobby_id = url[url.length - 2];
    $.ajax({
        'url': '/game-ajax/' + lobby_id + '/territory/get-all',
        'method': 'GET',
        success: function (data) {
            var response = $.parseJSON(JSON.stringify(data));
            $.each(response, function () {
                var el = document.createElement("area");
                el.setAttribute("shape", "poly");
                el.setAttribute("coords", this["coordinates"]);
                el.setAttribute("name", this["name"]);
                el.addEventListener("mouseover", mapMouseOver, true);
                el.addEventListener("mouseout", mapMouseOut, true);
                $("#map-regions")[0].append(el);
                var x = 0, xn = 0, y = 0, yn = 0;
                var c = this["coordinates"].split(",");
                for (i = 0; i < c.length; i += 2) {
                    x = x + parseInt(c[i]);
                    y = y + parseInt(c[i + 1]);
                    xn = xn + 1;
                    yn = yn + 1;
                }
                centerx = parseInt(x / xn);
                centery = parseInt(y / yn);
                el = document.createElement("div");
                el.setAttribute("class", "map-square");
                el.setAttribute("id", "square-" + this["name"]);
                el.setAttribute("name", this["name"]);
                el.style.left = centerx + "px";
                el.style.top = centery + "px";
                el.addEventListener("mouseover", mapMouseOver, true);
                el.addEventListener("mouseout", mapMouseOut, true);
                el.addEventListener("click", mapClick, true);
                $("#map-squares")[0].append(el);
            });
            updateGameInfo(response);
        }
    });
});

function mapMouseOver(e) {
    $("#map-hover-img")[0].src = "/static/map/border-" + e.target.getAttribute("name") + ".png";
}

function mapMouseOut(e) {
    $("#map-hover-img")[0].src = "/static/map/map.png";
}

function mapClick(e) {
    var name = e.target.getAttribute("name");
    var tx, ty;
    tx = event.pageX - parseInt($("#map")[0].style.marginLeft);
    ty = event.pageY - 35 - parseInt($("#map")[0].style.marginTop);
    $("#territory-information").text("");
    $("#territory-information").append('<span class="element">' + name + '</span>');
    $("#territory-information").append('<span class="element">Population: ' + territory_information[name]["population"] + '</span>');
    $("#territory-information").append('<span class="element">Army: ' + territory_information[name]["army"] + '</span>');
    $("#territory-information").append('<span class="element">Food: ' + territory_information[name]["food"] + '</span>');
    $("#territory-information").append('<span class="element">Gold: ' + territory_information[name]["gold"] + '</span>');
    if (territory_information[name]["owner"] == request_user)
        $("#territory-information").append('<span class="button"><a href="javascript:changePopulationArmy(\''+name+'\');">Change population/army<a></span>');
    if (territory_information[name]["owner"] != request_user && name in territory_neighbours)
        $("#territory-information").append('<span class="button"><a href="javascript:attack(\''+name+'\');">Attack</a></span>');
    $("#territory-information")[0].style.left = tx + "px";
    $("#territory-information")[0].style.top = ty + "px";
    $("#territory-information").show();
    e.stopPropagation();
}

$(document).ready(function () {
    if ($("#map").length == 0)
        return;
    $("#territory-information")[0].addEventListener("click", function (e) {
        e.stopPropagation();
    }, true);
});

var mapX = 0;
var mapY = 0;
var windowW = 0;
var windowH = 0;
var mapW = 2048;
var mapH = 2048;
var moveByX = 0;
var moveByY = 0;
$(document).ready(function () {
    if ($("#map").length == 0)
        return;
    $("#map")[0].style.marginLeft = "0px";
    $("#map")[0].style.marginTop = "0px";
    $("#map")[0].style.width = mapW + "px";
    $("#map")[0].style.height = mapH + "px";
    $("#map")[0].addEventListener("mousedown", mapMouseDown, true);
    $("#map")[0].addEventListener("mousemove", mapMouseMove, true);
    $("#map")[0].addEventListener("mouseout", function () {
        moveByX = 0;
        moveByY = 0;
    }, true);
    window.addEventListener("resize", windowResize, true);
    windowW = parseInt(window.getComputedStyle($("#map-holder")[0], null).getPropertyValue("width"));
    windowH = parseInt(window.getComputedStyle($("#map-holder")[0], null).getPropertyValue("height"));
    setTimeout("moveMapListener();", 50);
});
function moveMapListener() {
    var x, y;
    x = parseInt($("#map")[0].style.marginLeft);
    y = parseInt($("#map")[0].style.marginTop);
    x += moveByX;
    y += moveByY;
    mapMove(x, y);
    setTimeout("moveMapListener();", 50);
}
function mapMouseDown(event) {
    var tx, ty;
    tx = event.pageX - parseInt($("#map")[0].style.marginLeft);
    ty = event.pageY - 35 - parseInt($("#map")[0].style.marginTop);
    if (event.preventDefault) event.preventDefault();
    else event.returnValue = false;
    mapX = event.clientX;
    mapY = event.clientY;
    return false;
}
function mapMouseMove(event) {
    var x, y, mouseX, mouseY;
    x = parseInt($("#map")[0].style.marginLeft);
    y = parseInt($("#map")[0].style.marginTop);
    mouseX = event.clientX;
    mouseY = event.clientY;
    if (event.buttons == 0) {
        if (mouseX < 50) moveByX = 15 + (50 - mouseX);
        else if (mouseX > windowW - 50) moveByX = -15 + (windowW - 50 - mouseX);
        else moveByX = 0;

        if (mouseY < (50 + 35)) moveByY = 15 + (50 + 35 - mouseY);
        else if (mouseY > windowH + 35 - 50) moveByY = -15 + (windowH + 35 - 50 - mouseY);
        else moveByY = 0;
    }
    if (event.preventDefault) event.preventDefault();
    else event.returnValue = false;
    if (event.buttons != 1) {
        return false;
    }
    x += (mouseX - mapX);
    y += (mouseY - mapY);
    mapMove(x, y);
    mapX = mouseX;
    mapY = mouseY;
    event.stopPropagation();
    return false;
}
function windowResize(event) {
    windowW = parseInt(window.getComputedStyle($("#map-holder")[0], null).getPropertyValue("width"));
    windowH = parseInt(window.getComputedStyle($("#map-holder")[0], null).getPropertyValue("height"));
    x = parseInt($("#map")[0].style.marginLeft);
    y = parseInt($("#map")[0].style.marginTop);
    mapMove(x, y);
}
function mapMove(x, y) {
    if (windowW >= mapW)
        x = 0;
    else {
        if (x > 0) x = 0;
        else if (x < -mapW + windowW) x = -mapW + windowW;
    }
    if (windowH >= mapH)
        y = 0;
    else {
        if (y > 0) y = 0;
        else if (y < -mapH + windowH) y = -mapH + windowH;
    }
    $("#map")[0].style.marginLeft = x + "px";
    $("#map")[0].style.marginTop = y + "px";
}

function updateGameInfo(data) {
    territory_neighbours = {};
    $.each(data, function () {
        if (this["name"] == undefined)
            return;
        $("div[name*='" + this["name"] + "']")[0].style.background = this["colour"];
        if (territory_information[this["name"]] == undefined)
            territory_information[this["name"]] = {}
        if (this["id"] != undefined)
            territory_information[this["name"]]["id"] = this["id"];
        if (this["population"] != undefined)
            territory_information[this["name"]]["population"] = this["population"];
        if (this["army"] != undefined)
            territory_information[this["name"]]["army"] = this["army"];
        if (this["description"] != undefined)
            territory_information[this["name"]]["description"] = this["description"];
        if (this["food"] != undefined)
            territory_information[this["name"]]["food"] = this["food"];
        if (this["gold"] != undefined)
            territory_information[this["name"]]["gold"] = this["gold"];
        if (this["coordinates"] != undefined)
            territory_information[this["name"]]["coordinates"] = this["coordinates"];
        if (this["owner"] != undefined)
            territory_information[this["name"]]["owner"] = this["owner"];
        if (this["neighbours"] != undefined) {
            territory_information[this["name"]]["neighbours"] = this["neighbours"];
            if (this["owner"] == request_user) {
                for (i = 0; i < this["neighbours"].length; i++)
                    territory_neighbours[this["neighbours"][i]] = this["neighbours"][i];
            }
        }
        if (this["colour"] != undefined)
            territory_information[this["name"]]["colour"] = this["colour"];
    });
}
$(document).ready(function () {
    if ($("#map").length == 0)
        return;
    document.body.addEventListener("click", function () {
        $("#territory-information").hide();
        $("#territory-information").text("");
    }, false);
});
$(document).ready(function() {
    if($("#map").length==0)
        return;
    $("#population_value")[0].addEventListener("input",function(e) {
        $("#population_output").text(e.target.value);
        $("#army_value").val($("#total_pop_army").val()-e.target.value);
        $("#army_output").text($("#army_value").val());
    },true);
    $("#army_value")[0].addEventListener("input",function(e) {
        $("#army_output").text(e.target.value);
        $("#population_value").val($("#total_pop_army").val()-e.target.value);
        $("#population_output").text($("#population_value").val());
    },true);
    $("#change_dialog_submit")[0].addEventListener("click",function(e) {
        var territory_id=$("#territory_id").val();
        var population=$("#population_value").val();
        var army=$("#army_value").val();
        $.ajax({
            method: "POST",
            url: "/game-ajax/territory/set-population-army/",
            data: {
                "lobby_id": lobby_id,
                "territory_id": territory_id,
                "new_population": population,
                "new_army": army,
                "csrfmiddlewaretoken": csrf_token
            },
            success: function(data) {
                if(data.response=="error")
                    alert("There was an error while doing the request");
            }
        });
                
        $("#change-dialog").hide();
    },true);
    $("#change_dialog_cancel")[0].addEventListener("click",function(e) {
        $("#change-dialog").hide();
    },true);
});
function changePopulationArmy(name) {
    if(territory_information[name]==undefined)
        return;
    var totalPopulationArmy=territory_information[name]["population"]+territory_information[name]["army"]
    $("#territory_id").val(territory_information[name]["id"]);
    $("#population_output").text(territory_information[name]["population"]);
    $("#army_output").text(territory_information[name]["army"]);
    $("#population_value")[0].setAttribute("min","0");
    $("#population_value")[0].setAttribute("max",totalPopulationArmy);
    $("#population_value").val(territory_information[name]["population"]);
    $("#army_value")[0].setAttribute("min","0");
    $("#army_value")[0].setAttribute("max",totalPopulationArmy);
    $("#army_value").val(territory_information[name]["army"]);
    $("#total_pop_army").val(totalPopulationArmy);
    $("#change-dialog").show();
}
function attack(name) {
    var attack_from="";
    var army=-1;
    for(i=0;i<territory_information[name]["neighbours"].length;i++) {
        var terr=territory_information[name]["neighbours"][i];
        if(territory_information[terr]["owner"]==request_user && territory_information[terr]["army"]>army) {
            attack_from=terr;
            army=territory_information[terr]["army"];
        }
    }
    var t1_id=territory_information[name]["id"];
    var t2_id=territory_information[attack_from]["id"];
    $.ajax({
        method: "POST",
        url: "/game-ajax/army/attack/",
        data: {
            "lobby_id": lobby_id,
            "t1_id": t1_id,
            "t2_id": t2_id,
            "csrfmiddlewaretoken": csrf_token
        },
        success: function(data) {
            if(data.response=="error")
                alert("There was an error while doing the request");
            else if(data.response=="won")
                alert("You won!");
            else if(data.response=="lost")
                alert("You lost!");
        }
    });
}