function(doc) {
	if (doc.tags) {
		doc.tags.forEach(function(tag){
			emit(tag, 1);
		});
	}
}