function(doc) {
	if (doc.tags) {
		for (var idx in doc.tags) {
			emit([doc.tags[idx], doc.published], {
				title: doc.title, type: doc.type, tags: doc.tags
			});
		}
	}
}