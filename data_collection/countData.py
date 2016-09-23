# *******************************
# File 		: countData.py
# Author 	: Kavish N. Dahekar
# Email 	: kavishdahekar@gmail.com
# Details 	: script to count and analyse amount of data collected
# *******************************

import os

# get files from directory
files = os.listdir("data")

# define dictionary for storing counts
counts = {}
counts['0'] = 0
counts['1'] = 0
counts['2'] = 0
counts['3'] = 0
counts['4'] = 0
counts['5'] = 0
counts['6'] = 0
counts['7'] = 0
counts['8'] = 0
counts['9'] = 0
counts['a'] = 0
counts['b'] = 0
counts['c'] = 0
counts['d'] = 0
counts['e'] = 0
counts['f'] = 0
counts['g'] = 0
counts['h'] = 0
counts['i'] = 0
counts['j'] = 0
counts['k'] = 0
counts['l'] = 0
counts['m'] = 0
counts['n'] = 0
counts['o'] = 0
counts['p'] = 0
counts['q'] = 0
counts['r'] = 0
counts['s'] = 0
counts['t'] = 0
counts['u'] = 0
counts['v'] = 0
counts['w'] = 0
counts['x'] = 0
counts['y'] = 0
counts['z'] = 0

total = 0

# count and create html table
for file in files:
	if not file[:4] == "tmp_":
		file = file.split('_')[1]
		chars = list(file[:-4])
		for c in chars:
			counts[c] += 1
			total += 1

sh =	"<table>"\
		"<tr><td><b>total captchas so far</b></td><td><b>"+str(total/5)+"</b></td></tr>"\
		"<tr><td><b>total chars so far</b></td><td><b>"+str(total)+"</b></td></tr>"\
		"<table>"

ss =	"<table id='mtable' class='tablesorter'>"\
		"<thead><tr><th>character</th><th>data count</th></tr></thead>"\
		"<tbody>"\
		"<tr><td>0</td><td>"+str(counts['0'])+"</td></tr>"\
		"<tr><td>1</td><td>"+str(counts['1'])+"</td></tr>"\
		"<tr><td>2</td><td>"+str(counts['2'])+"</td></tr>"\
		"<tr><td>3</td><td>"+str(counts['3'])+"</td></tr>"\
		"<tr><td>4</td><td>"+str(counts['4'])+"</td></tr>"\
		"<tr><td>5</td><td>"+str(counts['5'])+"</td></tr>"\
		"<tr><td>6</td><td>"+str(counts['6'])+"</td></tr>"\
		"<tr><td>7</td><td>"+str(counts['7'])+"</td></tr>"\
		"<tr><td>8</td><td>"+str(counts['8'])+"</td></tr>"\
		"<tr><td>9</td><td>"+str(counts['9'])+"</td></tr>"\
		"<tr><td>a</td><td>"+str(counts['a'])+"</td></tr>"\
		"<tr><td>b</td><td>"+str(counts['b'])+"</td></tr>"\
		"<tr><td>c</td><td>"+str(counts['c'])+"</td></tr>"\
		"<tr><td>d</td><td>"+str(counts['d'])+"</td></tr>"\
		"<tr><td>e</td><td>"+str(counts['e'])+"</td></tr>"\
		"<tr><td>f</td><td>"+str(counts['f'])+"</td></tr>"\
		"<tr><td>g</td><td>"+str(counts['g'])+"</td></tr>"\
		"<tr><td>h</td><td>"+str(counts['h'])+"</td></tr>"\
		"<tr><td>i</td><td>"+str(counts['i'])+"</td></tr>"\
		"<tr><td>j</td><td>"+str(counts['j'])+"</td></tr>"\
		"<tr><td>k</td><td>"+str(counts['k'])+"</td></tr>"\
		"<tr><td>l</td><td>"+str(counts['l'])+"</td></tr>"\
		"<tr><td>m</td><td>"+str(counts['m'])+"</td></tr>"\
		"<tr><td>n</td><td>"+str(counts['n'])+"</td></tr>"\
		"<tr><td>o</td><td>"+str(counts['o'])+"</td></tr>"\
		"<tr><td>p</td><td>"+str(counts['p'])+"</td></tr>"\
		"<tr><td>q</td><td>"+str(counts['q'])+"</td></tr>"\
		"<tr><td>r</td><td>"+str(counts['r'])+"</td></tr>"\
		"<tr><td>s</td><td>"+str(counts['s'])+"</td></tr>"\
		"<tr><td>t</td><td>"+str(counts['t'])+"</td></tr>"\
		"<tr><td>u</td><td>"+str(counts['u'])+"</td></tr>"\
		"<tr><td>v</td><td>"+str(counts['v'])+"</td></tr>"\
		"<tr><td>w</td><td>"+str(counts['w'])+"</td></tr>"\
		"<tr><td>x</td><td>"+str(counts['x'])+"</td></tr>"\
		"<tr><td>y</td><td>"+str(counts['y'])+"</td></tr>"\
		"<tr><td>z</td><td>"+str(counts['z'])+"</td></tr>"\
		"</tbody>"\
		"</table>"

# print output, later grabbed by php code
print(sh)
print(ss)