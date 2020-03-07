window.onload=function() {
    var baseAPI = "http://localhost:3110/getresults";
    $.get(`${baseAPI}`, function(res) {
        var a = document.getElementById("map");
        var demPnt = 0;
        var repPnt = 0;
        res.forEach( (curRes) => {
            demPnt += curRes['result'] > 0 ? curRes['POINTS'] : 0;
            repPnt += curRes['result'] < 0 ? curRes['POINTS'] : 0;
            var color = curRes['result'] < 0 ? 'red' : 'blue';
            var state = a.getElementById(curRes['STATE']);
            state.setAttributeNS(null, 'fill', color);
        });
        console.log(demPnt);
        console.log(repPnt);
    });
};