from flask import Flask
import os
import json

cat='.'
def list_files(startpath):
    strfd = ''
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        strfd+=('{}{}/\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1);
        for f in files:
          strfd+=('{}{}\n'.format(subindent, f))
    return strfd



class NetController():
    def __init__(self):
        self.net_conf = ''
    
    def load_config(self, config):
        if config != '':
            try:
                self.net_conf == open(config,'r').read()
                pass
            except:
                pass
    def get_ports(self,nows):
        mynow = os.popen('./netstat -nltp').read()
        mass = mynow.split('\n')
        #print(mass)
        stringfds = ''
        jsonready = []
        name = 0
        pol = 0
        allsdf = []
        jsonnot = {}
        for line in mass:
            mass_all = line.split(' ')
            for me in mass_all:
                if me != '':
                    if me == 'name':
                        name +=1

                    if name ==1:
                        pol+=1
                        if pol >1:
                           allsdf.append(me)

        #['tcp', '0', '0', '0.0.0.0:902', '0.0.0.0:*', 'LISTEN', '1373/vmware-authdla', 
        # 'tcp', '0', '0', '127.0.0.1:40981', '0.0.0.0:*', 'LISTEN', '15157/vscodium', 
        # 'tcp', '0', '0', '127.0.0.1:631', '0.0.0.0:*', 'LISTEN', '567/cupsd', 
        # 'tcp', '0', '0', '0.0.0.0:7070', '0.0.0.0:*', 'LISTEN', '752/anydesk', 
        # 'tcp6', '0', '0', ':::902', ':::*', 'LISTEN', '1373/vmware-authdla', 
        # 'tcp6', '0', '0', '::1:631', ':::*', 'LISTEN', '567/cupsd']
        start = 0
        end = len(allsdf)-1
        while start<end:
            if start%7 == 0:
                jsonnot = {}
                jsonnot["type"] = allsdf[start-7]
                jsonnot["recvq"] = allsdf[start-6]
                jsonnot["sendq"] = allsdf[start-5]
                jsonnot["hostport"] = allsdf[start-4]
                jsonnot["host"] = allsdf[start-3]
                jsonnot["typli"] = allsdf[start-2]
                namepidmass = allsdf[start-1].split('/')
                jsonnot["pid"] = namepidmass[0]
                try:
                    jsonnot["name"] = namepidmass[1]
                    pass
                except:
                    jsonnot["name"] = '-'
                    pass
                jsonready.append(jsonnot)
            start+=1
        return str(jsonready).replace("'",'"')

template =	"""
<head>
<link rel="stylesheet" href="/styles">
<style>

</style>
<title>AdminPanel</title>
<meta charset="UTF-8">
</head>
<body>
<div class="header">
<div class="logo">
AdminPanel
</div>
<div class="menu">
<a class="menu__item" onclick="memory_display();">Memory</a>
<a class="menu__item" onclick="all_dir_display();">All Directory listing</a>
<a class="menu__item" onclick="port_display();">Ports</a>
<a class="menu__item" onclick="see_console();">Console</a>
</div>
</div>
<div class="about_it_panel">
</div>
<script>
	function kolom(text){
    return ('<td>'+text+'</td>');
	}
	function port_display(){
		let portdisp = document.getElementsByClassName('about_it_panel')[0];
		var xhr = new XMLHttpRequest();
xhr.open('GET', '/get_ports', false);
xhr.send();
if (xhr.status != 200) {
  console.log( xhr.status + ': ' + xhr.statusText );
} else {
  var polsd = '';
  var data = JSON.parse( xhr.responseText );
  for (let index = 0; index < data.length; index++) {
    const element = data[index];
    polsd = polsd + '<tr>'+kolom(data[index]['hostport'])+kolom(data[index]['typli'])+kolom(data[index]['pid'])+kolom(data[index]['name'])+'</tr>';
  }
  var pillow = `
<tr>
  <th class="th">HostPort</th>
  <th class="th">Mode</th>
  <th class="th">PID</th>
  <th class="th">Program Name<th>
  </tr>
`;
  portdisp.innerHTML = '<table>'+pillow+polsd+'</table>';
}
	}
	function all_dir_display(){
		let portdisp = document.getElementsByClassName('about_it_panel')[0];
		var xhr = new XMLHttpRequest();
xhr.open('GET', '/datas', false);
xhr.send();
if (xhr.status != 200) {
  console.log( xhr.status + ': ' + xhr.statusText );
} else {
  var polsd = '';
  var data = ( xhr.responseText );
	portdisp.innerText = data;
	portdisp.innerHTML = '<div class="code">' + portdisp.innerHTML + '</div>';
}
	}
	</script>
</body>
"""

styles = """
table {
width:100%;
margin-top:20px;
font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
font-size: 14px;
border-collapse: collapse;
text-align: center;
}
.th, td:first-child {
background: #AFCDE7;
color: white;
padding: 10px 20px;
}
.th, td {
border-style: solid;
border-width: 0 1px 1px 0;
border-color: white;
}
th:display:none;
td {
background: #D8E6F3;
}
.th:last-child {
text-align: left;
}
.logo {
    font-size: 28px;
    text-align: center;
}

.menu {
    justify-content: space-around;
    width: 100%;
    display: flex;
    flex-direction: column;
    border-top: 10px ridge;
    align-items: center;
    border-bottom: 10px ridge;
}
.code {
    border: 2px solid lightgray;
    padding: 14px;
    border-radius: 5px;
    margin-top: 11px;
}

.menu__item {
    border-bottom: 3px dotted;
    font-size: 20px;
    cursor: pointer;
}

.menu__item:hover {
    border-bottom: 3px solid;
}
"""

app = Flask(__name__)
net = NetController()
app.debug = True


@app.route('/')
def index():
    return template


@app.route('/get_ports')
def portget():
    return net.get_ports('Hello')

@app.route('/styles')
def style():
	return styles

@app.route('/datas')
def dataget():
	return list_files(cat)

if (__name__ == "__main__"):
    app.run(host="0.0.0.0",port=1028)