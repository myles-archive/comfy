function(doc) {
	if (doc.type == 'Post' && doc.tags) {
		for (var idx in doc.tags) {
			emit([doc.tags[idx], doc.published], {
				slug: doc.slug, title: doc.title, author: doc.author, published: doc.published, updated: doc.updated,
				summary: doc.summary, body: doc.body, tags: doc.tags, extended: doc.extended != '' ? '…' : null
			});
		}
	}
}