#Registers program with 2040 API.
#Returns:	an identifier token used to authenticate
#			later challenge submissions.
def register():
	#connect to http://challenge.code2040.org/api/register
	#POST: { "email":"<email here>", "github":"<github repo url>" }
	#Check your response, and return the response token.

#Posts a token to the given address, and reports the address' response.
#Parameters:
#	* token: The identifier returned from register().
#	* address: A URL to HTTP POST the token to.
#Returns:	The address' response as a string. This may be JSON data
#			that must be parsed.
def postToken(token, address):
	#connect to address
	#POST: { "token":"<token>" }
	#return response
	
#Performs the first challenge - reversing a string.
#Parameters:
#	* token: The identifier returned from register().
def revStr(token):
	#post token to http://challenge.code2040.org/api/getstring
	#Response is the string.
	#Reverse the string.
	#connect to http://challenge.code2040.org/api/validatestring
	#POST: { "token":"<token>", "string":"<reversed string>" }

#Performs the second challenge - finding an arbitrary string
#in a dictionary.
#Parameters:
#	* token: The identifier returned from register().
def findStr(token):
	#post token to http://challenge.code2040.org/api/haystack
	#Response is JSON:
	# { "needle":(string), "haystack":(array of strings) }
	#Find the 0-indexed index in haystack that matches needle.
	#connect to http://challenge.code2040.org/api/validateneedle
	#POST: { "token":"<token>", "needle":"<index of needle string>" }

#Performs the third challenge - filtering a dictionary
#by an arbitrary prefix.
#Parameters:
#	* token: The identifier returned from register().
def filterPrefix(token):
	#post token to http://challenge.code2040.org/api/prefix
	#Response is JSON:
	# { "prefix":(string), "array":(array of strings) }
	#Find all entries in array that DON'T start with prefix.
	#connect to http://challenge.code2040.org/api/validateprefix
	#POST: { "token":"<token>", "array":"<filtered array>" }

#Performs the fourth challenge - parsing and modifying 
#an ISO 8601 timestamp.
#Parameters:
#	* token: The identifier returned from register().
def timestamp(token):
	#post token to http://challenge.code2040.org/api/time
	#Response is JSON:
	# { "datestamp":(ISO 8601 datestamp, unknown subtype), "interval":(integer, seconds) }
	#Alter the datestamp such that it is ahead by interval seconds.
	#connect to http://challenge.code2040.org/api/validatetime
	#POST: { "token":"<token>", "datestamp":"<altered datestamp, ISO 8601>" }
	#Note that the altered datestamp must have the exact same subtype as the incoming datestamp.

#Gets grades for each API challenge.
#Returns:	A string containing grade information for each API challenge.
#Parameters:
#	* token: The identifier returned from register().
def getGrades(token):
	#post token to http://challenge.code2040.org/api/status
	#report our status as needed.

#Entry point for program.
def main():
	#Check our registration.
	token = register()
	#if it failed somehow, quit here.
	
	#Run all challenges.
	revStr(token)
	findStr(token)
	filterPrefix(token)
	timestamp(token)
	
	#Now check with the grade system.
	getGrades(token)

if __name__ == __main__:
	main()