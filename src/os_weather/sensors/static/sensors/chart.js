$("#chart-form").submit(function(event){
    event.preventDefault(); //prevent default action
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = $(this).serialize(); //Encode form elements for submission

    $.ajax({
        url : post_url,
        type: request_method,
        data : form_data
    }).done(function(response){ //
        //TODO
        //update the labels accord to the granularity
        //update the number of datasets accord to the signals
        //update the data of each signal
        //update the title text with the sensor name
    });
});

var lineChartData = {
	labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
	datasets: [{
		label: 'My First dataset',
		borderColor: window.chartColors.red,
		backgroundColor: window.chartColors.red,
		fill: false,
		data: [
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor()
		],
		yAxisID: 'y-axis-1',
	}, {
		label: 'My Second dataset',
		borderColor: window.chartColors.blue,
		backgroundColor: window.chartColors.blue,
		fill: false,
		data: [
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor(),
			randomScalingFactor()
		],
		yAxisID: 'y-axis-2'
	}]
};

window.onload = function() {
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = Chart.Line(ctx, {
		data: lineChartData,
		options: {
			responsive: true,
			hoverMode: 'index',
			stacked: false,
			title: {
				display: true,
				text: ''
			},
			scales: {
				yAxes: [{
					type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
					display: true,
					position: 'left',
					id: 'y-axis-1',
				}, {
					type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
					display: true,
					position: 'right',
					id: 'y-axis-2',

					// grid line settings
					gridLines: {
						drawOnChartArea: false, // only want the grid lines for one axis to show up
					},
				}],
			}
		}
	});
};