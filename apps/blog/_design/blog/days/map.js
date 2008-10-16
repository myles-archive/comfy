function(doc) {
	if (doc.type == 'Post') {
		var year = parseInt(doc.published.substr(0, 4), 10);
		var month = parseInt(doc.published.substr(5, 2), 10);
		var day = parseInt(doc.published.substr(8, 2), 10);
		emit([year, month, day], 1);
	}
}