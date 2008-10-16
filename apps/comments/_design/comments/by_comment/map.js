function(doc) {
	if (doc.comments) {
		for (var idx in doc.comments) {
			emit([doc.comment[idx].title], doc);
		}
	}
}