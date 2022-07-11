// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Porn", "Bitcoin", "Drug", "Counterfeit", "Murder", "Hack", "Weapon"],
    datasets: [{
      data: [20, 20, 20, 20, 20, 20, 20],
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#fba745','#28a225','#27a745','#28b745'],
    }],
  },
});
