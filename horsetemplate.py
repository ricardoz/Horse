head = """
<html>
    <head>
    
	
	<script type='text/javascript'>
	// FIND INDEX AND UPDATE IFRAME
    var counter = 0;
    var course = "red";
    var allHorses = {}
    var currentHorse = 2;
    
    var horseLinks =[];
    var allLinks = [];

    function findIndex(arr,obj) {
 	var ind = arr.indexOf(obj);
 	if (ind > -1){
		return ind;
	} else {
		return counter;
	}

}

function updateIframe(index){
     	
     	alert(horseLinks);
     	alert(index);
    
        if (index < 0){
            index += horseLinks.length;
        }
        
        counter = index;
        
        alert("update " + horseLinks[counter]);

        var url = horseLinks[index%horseLinks.length]['href'];
        
        alert("update url " + url);
        document.getElementById('horseFrame').src = url;
        return false;
    }
</script>

<script>
// Check if race matches course
// Return boolean to wnable combinations
var filterByCourse = function(race){
	return race['course'].toLowerCase() === course;
}

</script>

<script>
var changeHorse = function()
{
var mylist=document.getElementById("horses");
document.getElementById("horseName").innerHTML="<strong>"+mylist.options[mylist.selectedIndex].text+"</strong>";
currentHorse = allHorses[mylist.options[mylist.selectedIndex].text];
return  raceLinksFromHorse(currentHorse,filterByCourse);
}
</script>

<script>
// {"going": "GF", "distNext": "4.75L Norse Blues 8-8)", "jockey": "Connor Beasley", "weight": 118, "rpr": "*", "raceClass": "C2Hc", "///// price": 25.0, "pos": 6, "value": 16, "ts": "*", "course": "Thi", "href": "http://www.racingpost.com/horses/result_home.sd?race_id=////// 576401", "date": "04May13", "furlongs": 8, "OR": 92, "runners": 15}

function prettyPrintOneRace(race){
 	
	var pretty = '<a href="#" onclick="updateIframe(' + race["index"] + '); return false">' +
		race['date'] + " " + race['course'] + race['raceClass'] + " " + race['weight'] + "lbs " +
		race['pos'] + "/" + race['runners'] + " " + race['distNext'] + " " + race['price'] + " " +
		race['jockey'] + " " + race['OR'] + "</a>";
		
		return pretty;
}

var changeHorse = function()
{
 
var mylist=document.getElementById("horses");

document.getElementById("horseName").innerHTML="<strong>"+mylist.options[mylist.selectedIndex].text+"</strong>";
currentHorse = allHorses[mylist.options[mylist.selectedIndex].text];
return  raceLinksFromHorse(currentHorse,filterByCourse);
}

</script>
        
    </head>
    
    <body >
   
    
"""

body = """
    
    <table width="1200px" border="2" id="horseCarouselTable">

    <tr>

    <td rowspan="2" id="horseCarouselNavigation">
    <a href="#" onclick="updateIframe(counter+1); return false">
    <img src="leftArrow.gif"/>
	</a>
    <br />
    <a href="#" onclick="updateIframe(counter-1); return false"><img src="rightArrow.gif"/></a>
    </td>
    <td>Horse Form / Race Name</td>

    <td>H2H Horses</td>
    </tr>

    <tr>

    <td id= "horseName">Race name to appear here</td>

    <td id= "horseCarouselH2H">Other horses from both races here</td>
    </tr>

    </table>

    <br />


                <iframe
                	id = "horseFrame"
                    width="800"
                    height="600"
                    src="http://www.google.com"
                    frameborder="0"
                    

                ></iframe>
                
                
                <script>
    





function raceLinksFromHorse(horse, filter){

	var races = horse['races'];
	var raceIndex=1;
	var hrefs = [horse];
	
	var hcr = document.getElementById("horseCarouselH2H");
	var html = ""
	
	alert("start");
	for (i=0; i<races.length;i++){
	 	var race = races[i];
	 	if (filter(race)){
			hrefs.push(race);
			
			races[i]['index'] = raceIndex;
			
			raceIndex+=1;
			
			var n = prettyPrintOneRace(race);
			
			
			html = html + "<li>" + n + "</li>";
			
		}
	  	
	}
	
	var t = "<ul>" + html + "</ul>";

	
	hcr.innerHTML = "" + t;
	

	
	
	
	
	return hrefs;
}

horseLinks =  changeHorse()
alert("hl " + horseLinks);



    </script>
    </body>
</html> 

"""
