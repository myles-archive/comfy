function(doc) {
	if (doc.type == 'Event') {
		var year = parseInt(doc.start_date.substr(0, 4), 10);
		var month = parseInt(doc.start_date.substr(5, 2), 10);
		var day = parseInt(doc.start_date.substr(8, 2), 10);
		emit([year, month, day], 1);
	}
}