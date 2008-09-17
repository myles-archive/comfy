function(doc) {
	if (doc.type == 'Wiki') {
		emit([doc.title], doc);
	}
}
