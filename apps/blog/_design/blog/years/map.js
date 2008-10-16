function(doc) {
	if (doc.type == 'Post') {
		var year = parseInt(doc.published.substr(0, 4), 10);
		emit([year], 1);
	}
}