function(doc) {
	if (doc.type == 'FlatPage') {
		emit(doc.url, doc);
	}
}