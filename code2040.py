#Runs challenges for 2015 CODE2040.
#Requires Python 3.
import http.client
import json
import datetime

#Posts a string to the given address, and reports the address' response.
#Parameters:
#	* content: The JSON string to send.
#	* address: A URL to HTTP POST the token to.
#Returns:	The address' response as a string.
def post(content, address):
	conn = http.client.HTTPConnection(address)
	# Specify that the data is JSON,
	# and that we want a plaintext response.
	header = {	"Content-type": "application/json",
				"Accept":"text/plain"	}
	conn.request("POST", "", content, header)
	#Now get the response. We can do error checking here,
	#since we should expect a 200 OK response by checking
	#response.status.
	response = conn.getresponse()
	if response.status != 200:
		print("POST to " + address + " failed with code " + response.status + ": " + response.reason)
	#In any case, return the response content.
	return response.read()

#Registers program with 2040 API.
#Parameters:
#	* email: email address as a string.
#	* github: a Github repo as a string.
#Returns:	an identifier token used to authenticate
#			later challenge submissions.
def register(email, github):
	#connect to http://challenge.code2040.org/api/register
	#POST: { "email":"<email here>", "github":"<github repo url>" }
	content = json.dumps({"email":email, "github":github})
	token = post(content, "http://challenge.code2040.org/api/register")
	#Check response, and return the response token.
	return token

#Posts a token to the given address, and reports the address' response.
#Parameters:
#	* token: The identifier returned from register().
#	* address: A URL to HTTP POST the token to.
#Returns:	The address' response as a string. This may be JSON data
#			that must be parsed.
def postToken(token, address):
	#connect to address
	#POST: { "token":"<token>" }
	tokenStr = "{ \"token\":\"" + token + "\"}"
	#return response
	return post(tokenStr, address)
	
#Performs the first challenge - reversing a string.
#Parameters:
#	* token: The identifier returned from register().
def revStr(token):
	#post token to http://challenge.code2040.org/api/getstring
	str = postToken(token, "http://challenge.code2040.org/api/getstring")
	#Response is the string.
	#Reverse the string like this is 201!
	revStr = str[::-1]
	#connect to http://challenge.code2040.org/api/validatestring
	#POST: { "token":"<token>", "string":"<reversed string>" }
	content = json.dumps({"token":token, "string":revStr})
	post(content, "http://challenge.code2040.org/api/validatestring")
	

#Performs the second challenge - finding an arbitrary string
#in a dictionary.
#Parameters:
#	* token: The identifier returned from register().
def findStr(token):
	#post token to http://challenge.code2040.org/api/haystack
	data = postToken(token, "http://challenge.code2040.org/api/haystack")
	#Response is JSON:
	# { "needle":(string), "haystack":(array of strings) }
	#Parse it out.
	parsed = json.loads(data)
	needle = parsed["needle"]
	haystack = parsed["haystack"]
	#Find the 0-indexed index in haystack that matches needle.
	idx = haystack.index(needle)
	#connect to http://challenge.code2040.org/api/validateneedle
	#POST: { "token":"<token>", "needle":"<index of needle string>" }
	content = json.dumps({"token":token, "needle":idx})
	post(content, "http://challenge.code2040.org/api/validateneedle")

#Performs the third challenge - filtering a dictionary
#by an arbitrary prefix.
#Parameters:
#	* token: The identifier returned from register().
def filterPrefix(token):
	#post token to http://challenge.code2040.org/api/prefix
	data = postToken(token, "http://challenge.code2040.org/api/prefix")
	#Response is JSON:
	# { "prefix":(string), "array":(array of strings) }
	parsed = json.loads(data)
	prefix = parsed["prefix"]
	array = parsed["array"]
	results = []
	#Find all entries in array that DON'T start with prefix.
	for str in array:
		if not str.startswith(prefix):
			results.append(str)
	#connect to http://challenge.code2040.org/api/validateprefix
	#POST: { "token":"<token>", "array":"<filtered array>" }
	content = json.dumps({"token":token, "array":results})
	post(content, "http://challenge.code2040.org/api/validateprefix")

def alterTimestamp(datestamp, interval)
	#See if there's a T to indicate time.
	#If not, we can't modify by seconds, return the datestamp.
	if not "T" in datestamp:
		return datestamp
	#Otherwise, see if there's a timezone designator:
	#	* A "Z" at the end
	#	* A "+" or "-" after the time code
	#In any of these cases, save the timecode data.
	#For "Z" this will be everything between the time code and "Z",
	#for other markers this will be everything after the marker.
	fmt = ""
	if "Z" in datestamp:
		fmt = "%Y-%m-%dT%M:%S:%fZ"
	else if "+" in datestamp or "-" in datestamp:
		#This part will almost certainly have an exception in Python 2,
		#but I don't think we're supposed to use external libraries.
		fmt = "%Y-%m-%dT%M:%S:%f%z"
	dt = datetime.datetime.strptime(datestamp, fmt)
	#Update the interval...
	dt + datetime.timedelta(seconds=interval)
	#And return the new time in the format we received.
	return dt.strftime(fmt)
	
	
	
#Performs the fourth challenge - parsing and modifying 
#an ISO 8601 timestamp.
#Parameters:
#	* token: The identifier returned from register().
def timestamp(token):
	#post token to http://challenge.code2040.org/api/time
	data = postToken(token, "http://challenge.code2040.org/api/time")
	#Response is JSON:
	# { "datestamp":(ISO 8601 datestamp, unknown subtype), "interval":(integer, seconds) }
	parsed = json.loads(data)
	datestamp = parsed["datestamp"]
	interval = int(parsed["interval"])
	#Alter the datestamp such that it is ahead by interval seconds.
	result = alterTimestamp(datestamp, interval)
	#connect to http://challenge.code2040.org/api/validatetime
	#POST: { "token":"<token>", "datestamp":"<altered datestamp, ISO 8601>" }
	#Note that the altered datestamp must have the exact same subtype as the incoming datestamp.
	content = json.dumps({"token":token, "datestamp":result})
	post(content, "http://challenge.code2040.org/api/validatetime")

#Gets grades for each API challenge.
#Returns:	A string containing grade information for each API challenge.
#Parameters:
#	* token: The identifier returned from register().
def getGrades(token):
	#post token to http://challenge.code2040.org/api/status
	#report our status as needed.
	grades = postToken(token, "http://challenge.code2040.org/api/status")
	print("Grades are: " + grades)

#Entry point for program.
def main():
	#Setup program constants.
	email = "leumi1@umbc.edu"
	github = "https://github.com/jTitor/code2040_Jan15.git"
	
	#Check our registration.
	token = register(email, github)
	print("Token is: " + token)
	#if it failed somehow, quit here.
	
	#Run all challenges.
	print("Running challenges..."
	revStr(token)
	findStr(token)
	filterPrefix(token)
	timestamp(token)
	
	#Now check with the grade system.
	getGrades(token)

if __name__ == __main__:
	main()