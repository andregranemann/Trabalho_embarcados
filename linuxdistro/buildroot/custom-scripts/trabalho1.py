import SimpleHTTPServer
import SocketServer
import os.path
import os, platform, subprocess, re
import datetime
import psutil

def get_processor_name():
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + '/usr/sbin'
        command ="sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(command).strip()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo"
        all_info = subprocess.check_output(command, shell=True).strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub( ".*model name.*:", "", line,1)
    return ""

def get_cpu_usage():
    last_idle = last_total = 0
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    utilisation = 100*(1-idle_delta / total_delta)
    return utilisation

def get_uptime():
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"

     total_seconds = float(contents[0])
     return total_seconds;

def getRAMinfo():
			
			p = os.popen('free')
			i = 0
			while 1:
				i = i + 1
				line = p.readline()
        
				if i==2:
					memT=int(line.split()[1])/1000
					memU=int(line.split()[2])/1000
					mem = str(memU) + "Mb /" + str(memT) + "Mb"
					return mem

def getPID():
	list_proc = ""
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
		except psutil.NoSuchProcess:
			pass
		else:
			list_proc += "<p>" + str(pinfo) + "</p>"
	return list_proc    


#arquivo = open('index.html', 'w')
#arquivo.write(html)
#arquivo.close()


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # Build the html file for every connection.    
    def makeindex(self):
        tofile= """<!DOCTYPE html>
        <html>
        <body>

        <h1>Target do sistema</h1>

        <p> Uptime do sistema: %s segundos</p>

        <p> Nome do processador: %s </p>

        <p> Uso do processador: %s </p>

        <p> RAM usada / total: %s </p>

        <p> Versao do sistema: %s </p>

        <p>Relatorio gerado em: %s</p>
        
        <p> Lista de Processos em execucao:</p>
        %s
       
        </body>
        </html>
        """ % (str(get_uptime()), str(get_processor_name()), str(round(get_cpu_usage(), 2)) + '%', getRAMinfo(),
               str(platform.version()), str(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')), str(getPID()))
        f = open("index.html", "w")
        f.write(tofile)
        f.close()
        return

    # Method http GET.
    def do_GET(self):
        self.makeindex()
        self.path = '/index.html'
        return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


# Start the webserver.
Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
server.serve_forever()

