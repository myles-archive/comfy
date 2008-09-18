function(doc) {
	if (doc.tags) {
		for (var idx in doc.tags) {
			emit(doc.tags[idx], 1);
		}
	}
}