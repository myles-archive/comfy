function(doc) {
	var types = new Array ( 'Wiki', 'Post', 'Bookmark' )
	if (doc.type == types) {
		emit([doc.title], doc);
	}
}