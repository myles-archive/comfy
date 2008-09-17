function(doc) {
	if (doc.type == 'Post' && doc.tags) {
		for (var idx in doc.tags) {
			emit(doc.tags[idx], 1);
		}
	}
}