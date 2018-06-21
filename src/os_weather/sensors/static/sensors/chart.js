var chart = null;

$("#chart-form").submit(function(event){
    event.preventDefault();
    var post_url = $(this).attr("action");
    var request_method = $(this).attr("method");
    var form_data = $(this).serialize();

    var chartColors = [
	    'rgb(255, 99, 132)',
	    'rgb(255, 159, 64)',
	    'rgb(255, 205, 86)',
	    'rgb(75, 192, 192)',
	    'rgb(54, 162, 235)',
	    'rgb(153, 102, 255)',
	    'rgb(201, 203, 207)'
    ];

    $.ajax({
        url : post_url,
        type: request_method,
        data : form_data
    }).done(function(response){
        var labels_final = [];
        var datasets = [];
        var scales = [];
        $.each(response, function(index, item){
            var labels = [];
            var data = [];
            $.each(item, function(item_index, tuple){
                data.push(tuple[1]);
                labels.push(tuple[0]);
            });

            var colorIndex = Math.floor(Math.random()*chartColors.length);
            var color = chartColors[colorIndex];
            chartColors.splice(colorIndex, 1);
            var dataset = {
		        label: index,
		        borderColor: color,
		        backgroundColor: color,
		        fill: false,
		        data: data,
		        yAxisID: index,
        	};
        	var scale =  {
			    type: 'linear',
				display: true,
				position: 'left',
				id: index,
			}

            datasets.push(dataset);
            scales.push(scale);
            labels_final = labels;
        });
        chart = newChart(datasets, labels_final, scales);
    });
});


var newChart = function(datasets, labels, scales){
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'line',
	    data:  {
            labels: labels,
            datasets: datasets
        },
    	options: {
    		responsive: true,
    		hoverMode: 'index',
    		stacked: false,
    		title: {
    			display: true,
	    		text: 'OS-WEATHER'
    		},
    		scales: {
				yAxes: scales,
			},
	    }
    });
    return chart;
};