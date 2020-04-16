from background_task import background

# repeat task hourly
@background(repeat=Task.HOURLY)
def request_instagram():
	# for (user : linqUsers):
	#	GET last ~20 Instagram posts
	#	for (comment : comments):
	#		POST comment to Linq API (overwrite)

