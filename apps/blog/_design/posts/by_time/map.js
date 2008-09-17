function(doc) {
	if (doc.type == 'Post') {
		emit([doc.published], {
			slug: doc.slug, title: doc.title, author: doc.author, summary: doc.summary,
			body: doc.body, published: doc.published, updated: doc.updated, extended: doc.extended != '' ? '…' : null,
			tags: doc.tags, allow_comments: doc.allow_comments, num_comments: doc.num_comments,
			allow_pings: doc.allow_pings, num_pings: doc.num_pings
		});
	}
}