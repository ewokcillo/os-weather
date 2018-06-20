var chart = null;

$("#chart-form").submit(function(event){
    event.preventDefault(); //prevent default action
    var post_url = $(this).attr("action"); //get form action url
    var request_method = $(this).attr("method"); //get form GET/POST method
    var form_data = $(this).serialize(); //Encode form elements for submission

    $.ajax({
        url : post_url,
        type: request_method,
        data : form_data
    }).done(function(response){
        var labels_final = [];
        var datasets = [];
        $.each(response, function(index, item){
            var labels = [];
            var data = [];
            $.each(item, function(item_index, tuple){
                data.push(tuple[1]);
                labels.push(tuple[0]);
            });
            var dataset = {
		        label: index,
		        borderColor: window.chartColors.red,
		        backgroundColor: window.chartColors.red,
		        fill: false,
		        data: data,
    		    yAxisID: index,
        	};
            datasets.push(dataset);
            labels_final = labels;
        });
        chart = newChart(datasets, labels_final);
    });
});


var newChart = function(datasets, labels){
    var ctx = document.getElementById('canvas').getContext('2d');
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
	    }
    });
    return chart;
};