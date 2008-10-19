function(doc) {
	if (doc.type == 'Bookmark') {
		emit([doc.published], {
			title: doc.title, author: doc.author, body: doc.body,
			published: doc.published
		});
	}
}