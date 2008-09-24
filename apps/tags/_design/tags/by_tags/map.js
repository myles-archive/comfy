function(doc) {
	if (doc.tags) {
		for (var idx in doc.tags) {
			emit([doc.tags[idx], doc.published], {
				title: doc.title, tags: doc.tags != '' ? '…' : null
			});
		}
	}
}