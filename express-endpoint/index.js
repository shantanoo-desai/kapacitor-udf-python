var express = require("express");

var app = express();

var bodyParser = require("body-parser");
var urlencodedParser = bodyParser.urlencoded({extended: true});
var jsonParser = bodyParser.json();
var port = 30001;
app.use(jsonParser);

app.post('/kapacitor', jsonParser, function(request, response) {
    console.log(request.body.series[0]);
    response.send();
});

app.listen(port);

console.log('Express App is listening to port '+ port);
