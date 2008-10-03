function(doc) {
	emit(Date.parse(doc.created), {
		type: doc.type, created: doc.created
	})
}