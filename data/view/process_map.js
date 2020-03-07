window.onload=function() {
    var a = document.getElementById("map");
    console.log(a);
    var AZ = a.getElementById("AZ");
    console.log(AZ);
    //sampleMap.setAttribute("fill", "lime");
    AZ.setAttributeNS(null, 'fill', '#f06');
	//svgItem.setAttribute("fill", "lime");
};


// var curSvg = document.getElementsByTagName('svg')[0];
// var rect = document.getElementById("AZ");
// rect.setAttributeNS(null, 'fill', '#f06');