function(doc) {
	if (doc.published) {
		emit(doc.published, {
			title: doc.title != '' ? doc.title : null,
			type: doc.type, created: doc.created,
			published: doc.published, tags: doc.tags,
			body: doc.body
		})
	}
}