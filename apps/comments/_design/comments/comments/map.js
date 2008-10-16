function(doc) {
	if (doc.comments) {
		for (var idx in doc.comments) {
			if (doc.comments[idx].is_spam == false) {
				emit([doc.title], {
					commnet:		doc.comments[idx].comment,
					author_name:	doc.comments[idx].author.name,
					author_url:		doc.comments[idx].author.url,
					time:			doc.comments[idx].time
				});	
			}
		}
	}
}