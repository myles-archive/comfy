function(doc) {
	if (doc.type == 'Event') {
		var year = parseInt(doc.published.substr(0, 4), 10);
		var month = parseInt(doc.published.substr(5, 2), 10);
		var day = parseInt(doc.published.substr(8, 2), 10);
		emit([year, month, day, doc.start_date], {
			title: doc.title, start_date: doc.start_date, start_time: doc.start_time,
			end_date: doc.end_date, end_time: doc.end_time
		});
	}
}