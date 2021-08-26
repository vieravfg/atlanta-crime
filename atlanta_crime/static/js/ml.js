d3.json("/prediction").then(prediction_ml => {
  var result = prediction_ml;
  console.log(result);
  var button = d3.select('#result');
  //console.log(button);
  //console.log(calendar)
  function changeDate() {
      //clear the table
      d3.select("#pred_result").selectAll("td").remove();
      // Prevent the page from refreshing
      //d3.event.preventDefault();
      // grab the values of the input fields
      calendarstart = d3.select('#start');
      calendarend = d3.select('#end');
      var startdate = calendarstart.property("value");
      var enddate = calendarend.property("value");
      //create a filter dictionary
      var filters = new Object();
      //assign key and value pair to the dictionary based on user inputs
      if (startdate !== ""){
      filters["startdate"]=startdate;
      }
      if (enddate !== ""){
      filters["enddate"]=enddate;
      }
      console.log(filters);
      filters.startdate = new Date(filters.startdate);
      filters.enddate = new Date(filters.enddate);
      //call seaerch function to return filtered data 
      var filteredData = result.filter(pred => (new Date(pred.Date) >= filters.startdate)&&new Date(pred.Date)<=filters.enddate);
      //display filtered data in the html table
      tbody = d3.select("tbody")
      var date =[];
      var arima_result = [];
      var prophet_result = [];
      function convertUTCDateToLocalDate(date) {
          var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);
      
          var offset = date.getTimezoneOffset() / 60;
          var hours = date.getHours();
      
          newDate.setHours(hours - offset);
      
          return newDate;   
      }
      filteredData.forEach(function(row){
          row.Date = convertUTCDateToLocalDate(new Date(row.Date));
          row.Date = new Date(row.Date);
          year = row.Date.getFullYear();
          month = row.Date.getMonth()+1;
          d = row.Date.getDate();
          row.Date = `${year}-${month}-${d}`;
          date.push(row.Date);
          arima_result.push(row.arima_value);
          prophet_result.push(row.prophet_value);
          var tr = tbody.append("tr");
          Object.entries(row).forEach(function([key, value]){
              var cell =tr.append("td");
              cell.text(value);
              });
      });
      var trace1 = {
          x: date,
          y: arima_result,
          type: 'scatter',
          name: 'ARIMA Result'
        };
        
        var trace2 = {
          x: date,
          y: prophet_result,
          type: 'scatter',
          name: 'Phrophet Result'
        };
        
        var data = [trace1, trace2];
        var layout = {
          title:'Compare ARIMA and Prophet Results',
        };
        Plotly.newPlot('myDiv', data,layout);
  };
  button.on("click", changeDate);
});

