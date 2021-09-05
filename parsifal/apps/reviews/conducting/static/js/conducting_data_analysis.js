google.load('visualization', '1.0', {'packages':['corechart']});
google.setOnLoadCallback(drawChartCallback);

function drawChartCallback() {
  drawChart();
  drawYearLines();
}

function drawPieChart(rows) {
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Source');
  data.addColumn('number', 'Number of Aticles');
  data.addRows(rows);
  var options = {'height': 400};
  var chart = new google.visualization.PieChart(document.getElementById('articles-selection-pie'));
  chart.draw(data, options);
}

function drawColumnChart(rows) {
  var data = google.visualization.arrayToDataTable(rows);
  var options = {
    vAxis: {title: 'Number of Articles',  titleTextStyle: {color: '#3A3D40'}},
    'height': 400
  };
  var chart = new google.visualization.ColumnChart(document.getElementById('articles-selection-column'));
  chart.draw(data, options);
}

function drawLineChart(rows) {
  var data = google.visualization.arrayToDataTable(rows);
  var options = {
    vAxis: {title: 'Number of Articles',  titleTextStyle: {color: '#3A3D40'}},
    'height': 400
  };
  var chart = new google.visualization.LineChart(document.getElementById('articles-selection-line'));
  chart.draw(data, options);
}

function drawChart() {
  $.ajax({
    url: '/reviews/conducting/articles_selection_chart/',
    data: {'review-id': $("#review-id").val()},
    type: 'get',
    cache: false,
    beforeSend: function () {
      $("#articles-selection-pie").spinner(false);
      $("#articles-selection-column").spinner(false);
    },
    success: function (data) {
      var source_data = data.split(",");
      var rows_pie = [];
      var rows_chart = [['Source', 'Selected', 'Accepted']];
      for (var i = source_data.length - 1; i >= 0; i--) {
        row = source_data[i].split(":");
        rows_pie.push([row[0], parseInt(row[1])]);
        rows_chart.push([row[0], parseInt(row[1]), parseInt(row[2])]);
      };
      drawPieChart(rows_pie);
      drawColumnChart(rows_chart);
    },
    complete: function () {
      $("#articles-selection-pie").spinner();
      $("#articles-selection-column").spinner();
    }
  });
}

function drawYearLines() {
  $.ajax({
    url: '/reviews/conducting/articles_per_year/',
    data: {'review-id': $("#review-id").val()},
    type: 'get',
    cache: false,
    beforeSend: function () {
      $("#articles-selection-line").spinner(false);
    },
    success: function (data) {
      var source_data = data.split(",");
      var rows = [['Year', 'Number of Articles']];
      for (var i = source_data.length - 1; i >= 0; i--) {
        row = source_data[i].split(":");
        rows.push([row[0], parseInt(row[1])]);
      };
      drawLineChart(rows);
    },
    complete: function () {
      $("#articles-selection-line").spinner();
    }
  });
}