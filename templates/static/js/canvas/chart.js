window.onload = function () {

	var pieChart = new CanvasJS.Chart("pie-chartContainer", {
		animationEnabled: true,
		data: [{
			type: "doughnut",
			startAngle: 60,
			//innerRadius: 60,
			indexLabelFontSize: 15,
			indexLabel: "{label} - #percent%",
			toolTipContent: "<b>{label}:</b> {y} (#percent%)",
			dataPoints: [
				{ y: 67, label: "Inbox" },
				{ y: 28, label: "Archives" },
				{ y: 10, label: "Labels" },
				{ y: 7, label: "Drafts"},
				{ y: 15, label: "Trash"},
				{ y: 6, label: "Spam"}
			]
		}]
	});

	var lineChart = new CanvasJS.Chart("line-chartContainer", {
		
		toolTip: {
			shared: true
		},
		legend: {
			cursor: "pointer",
			itemclick: toggleDataSeries
		},
		data: [{
			type: "line",
			name: "Lorem 1",
			color: "#369EAD",
			showInLegend: true,
			axisYIndex: 1,
			dataPoints: [
				{ x: new Date(2017, 00, 7), y: 85.4 }, 
				{ x: new Date(2017, 00, 14), y: 92.7 },
				{ x: new Date(2017, 00, 21), y: 64.9 },
				{ x: new Date(2017, 00, 28), y: 58.0 },
				{ x: new Date(2017, 01, 4), y: 63.4 },
				{ x: new Date(2017, 01, 11), y: 69.9 },
				{ x: new Date(2017, 01, 18), y: 88.9 },
				{ x: new Date(2017, 01, 25), y: 66.3 },
				{ x: new Date(2017, 02, 4), y: 82.7 },
				{ x: new Date(2017, 02, 11), y: 60.2 },
				{ x: new Date(2017, 02, 18), y: 87.3 },
				{ x: new Date(2017, 02, 25), y: 98.5 }
			]
		},
		{
			type: "line",
			name: "Lorem 2",
			color: "#C24642",
			axisYIndex: 0,
			showInLegend: true,
			dataPoints: [
				{ x: new Date(2017, 00, 7), y: 32.3 }, 
				{ x: new Date(2017, 00, 14), y: 33.9 },
				{ x: new Date(2017, 00, 21), y: 26.0 },
				{ x: new Date(2017, 00, 28), y: 15.8 },
				{ x: new Date(2017, 01, 4), y: 18.6 },
				{ x: new Date(2017, 01, 11), y: 34.6 },
				{ x: new Date(2017, 01, 18), y: 37.7 },
				{ x: new Date(2017, 01, 25), y: 24.7 },
				{ x: new Date(2017, 02, 4), y: 35.9 },
				{ x: new Date(2017, 02, 11), y: 12.8 },
				{ x: new Date(2017, 02, 18), y: 38.1 },
				{ x: new Date(2017, 02, 25), y: 42.4 }
			]
		},
		{
			type: "line",
			name: "Lorem 3",
			color: "#7F6084",
			axisYType: "secondary",
			showInLegend: true,
			dataPoints: [
				{ x: new Date(2017, 00, 7), y: 42.5 }, 
				{ x: new Date(2017, 00, 14), y: 44.3 },
				{ x: new Date(2017, 00, 21), y: 28.7 },
				{ x: new Date(2017, 00, 28), y: 22.5 },
				{ x: new Date(2017, 01, 4), y: 25.6 },
				{ x: new Date(2017, 01, 11), y: 45.7 },
				{ x: new Date(2017, 01, 18), y: 54.6 },
				{ x: new Date(2017, 01, 25), y: 32.0 },
				{ x: new Date(2017, 02, 4), y: 43.9 },
				{ x: new Date(2017, 02, 11), y: 26.4 },
				{ x: new Date(2017, 02, 18), y: 40.3 },
				{ x: new Date(2017, 02, 25), y: 54.2 }
			]
		}]
	});

	lineChart.render();
	pieChart.render();

	function toggleDataSeries(e) {
		if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
			e.dataSeries.visible = false;
		}
		else {
			e.dataSeries.visible = true;
		}
		chart.render();
	}

}



