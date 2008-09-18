function(doc) {
	if (doc.type == 'Post') {
		emit([doc.updated], null);
	}
}