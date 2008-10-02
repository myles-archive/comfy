function(doc) {
	if (doc.type == 'Note' && doc.private == false) {
		emit([doc.created], {
			body: doc.body, updated: doc.updated, created: doc.created,
			tags: doc.tags, private: doc.private
		});
	}
}