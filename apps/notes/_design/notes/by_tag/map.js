function(doc) {
	if (doc.type == 'Note' && doc.private == false && doc.tags) {
		for (var idx in doc.tags) {
			emit([doc.tags[idx], doc.updated], {
				body: doc.body, updated: doc.updated, created: doc.created,
				tags: doc.tags, private: doc.private
			});
		}
	}
}