function(doc) {
	if (doc.published) {
		emit(doc.published, {
			type: doc.type, created: doc.created, published: doc.published
		})
	}
}