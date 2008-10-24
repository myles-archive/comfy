function(doc) {
	if (doc.type == 'Event') {
		var year = parseInt(doc.start_date.substr(0, 4), 10);
		emit([year], 1);
	}
}