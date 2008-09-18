function(doc) {
	if (doc.tags) {
		for (var idx in doc.tags) {
			emit([doc.tags[idx], doc.published], {
				title: doc.title, author: doc.author.name, published: doc.published,
				updated: doc.updated, tags: doc.tags != '' ? '…' : null
			});
		}
	}
}