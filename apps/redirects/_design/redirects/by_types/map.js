function(doc) {
	if (doc.type) {
		emit([doc.type], {
			title: doc.title,
		});
	}
}