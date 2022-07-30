import colorama, subprocess, typer, datetime, time, os, json, platform

colorama.init()

def delvalue(value, delval):
    n = 0
    for i in range(0, len(value)):
        if value[i] == delval:
            n = i
            break
    try:
        del value[n]
        return value
    except: return 'This file is not valid !'

def getDateString():
    date = datetime.datetime.now()
    return f'{date.year}.year/{date.month}.month/{date.day}.day/{date.hour}.hour/{date.minute}.min/{date.second}.second/{date.microsecond}.microsecond'

def readPymon():
    fr = ''
    with open('.pymon/init.json', 'r') as f:
        fr = json.loads(f.read())
        f.close()
    return fr

def writePymon(data):
    with open('.pymon/init.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
        f.close()
    return

def start(filename):
    work = [f'{colorama.Fore.GREEN}[PYMON] starting', f'{colorama.Fore.GREEN}[PYMON] 4.0.0', f'{colorama.Fore.GREEN}[PYMON] ...', f'{colorama.Fore.YELLOW}###### - PYMON - RUN => {colorama.Fore.CYAN}"{filename}"{colorama.Fore.GREEN} - ######{colorama.Fore.GREEN} Start Date => {getDateString()}\n']
    for data in work:
        time.sleep(0.3)
        print(data)
    if '.pymon' in os.listdir('./'):
        os.remove('.pymon/init.json')
        os.rmdir('.pymon')
    os.mkdir('.pymon')
    with open('.pymon/init.json', 'w') as f:
        f.write(json.dumps(json.loads('{"filename": [], "re_run": []}'), indent=4))
        f.close()

    return

def cls():
    osname = platform.system()
    if osname == 'Linux':
        os.system('clear')
    else: os.system('cls')

# cls()

pyversion = ''

# cls()

def getVersion():
    global pyversion
    return pyversion

def stopText(filename):
    print(f'\n{colorama.Fore.YELLOW}###### - PYMON - Stop => {colorama.Fore.CYAN}"{filename}"{colorama.Fore.GREEN} - ######{colorama.Fore.GREEN} Stop Date => {getDateString()}\n')

def reStart(filename):
    print(f'\n{colorama.Fore.YELLOW}###### - PYMON - ReRun => {colorama.Fore.CYAN}"{filename}"{colorama.Fore.GREEN} - ######{colorama.Fore.GREEN} ReRun Date => {getDateString()}\n')

def checkFile(filename, method='None'):
    try:
        with open(filename, 'r') as f:
            filetext = f.read()
            f.close()
            if method == 'read':
                return filetext
            else: return ''
    except: return 'File not found !'

app = typer.Typer()

@app.command()
def run(filename):
    global pyversion
    while True:
        pyversion = input(f'{colorama.Fore.GREEN}Are you using Python10 or newer? (y/n): ')
        if pyversion == 'y':
            pyversion = 'py'
            break
        if pyversion == 'n':
            pyversion = 'python'
            break
    text = checkFile(filename, method='read')
    if text != 'File not found !':
        start(filename)
        app = subprocess.Popen([getVersion(), filename])
        jdata = readPymon()
        jdata['filename'].append(filename)
        writePymon(jdata)
        try:
            while True:
                jdata = readPymon()
                time.sleep(0.5)
                if filename in jdata['re_run']:
                    with open(filename, 'r') as f:
                        fr = f.read()
                        jdata = readPymon()
                        res = delvalue(jdata['re_run'], filename)
                        if res != 'This file is not valid !':
                            jdata['re_run'] = res
                        else: pass
                        writePymon(jdata)
                        reStart(filename)
                        app.terminate()
                        app = subprocess.Popen([getVersion(), filename])
                        text = fr
                        f.close()
                else: pass
                if filename in jdata['filename']:
                    with open(filename, 'r') as f:
                        fr = f.read()
                        if text == fr:
                            pass
                        else:
                            app.terminate()
                            reStart(filename)
                            app = subprocess.Popen([getVersion(), filename])
                            text = fr
                        f.close()
                else:
                    stopText(filename)
                    app.terminate()
                    break
        except:
            app.terminate()
            stopText(filename)

    else:
        print(f'{colorama.Fore.RED}{text}')

@app.command()
def reRun(filename):
    jdata = readPymon()
    jdata['re_run'].append(filename)
    writePymon(jdata)

@app.command()
def runWithCommand(filename, command):
    global pyversion
    while True:
        pyversion = input(f'{colorama.Fore.GREEN}Are you using Python10 or newer? (y/n): ')
        if pyversion == 'y':
            pyversion = 'py'
            break
        if pyversion == 'n':
            pyversion = 'python'
            break
    text = checkFile(filename, method='read')
    if text != 'File not found !':
        start(filename)
        newlist = [getVersion(), filename]
        for i in command.split(' '):
            newlist.append(i)
        app = subprocess.Popen(newlist)
        jdata = readPymon()
        jdata['filename'].append(filename)
        writePymon(jdata)
        try:
            while True:
                jdata = readPymon()
                time.sleep(0.5)
                if filename in jdata['re_run']:
                    with open(filename, 'r') as f:
                        fr = f.read()
                        jdata = readPymon()
                        jdata['re_run'] = []
                        writePymon(jdata)
                        reStart(filename)
                        app.terminate()
                        newlist = [getVersion(), filename]
                        for i in command.split(' '):
                            newlist.append(i)
                        app = subprocess.Popen(newlist)
                        text = fr
                        f.close()
                else: pass
                if filename in jdata['filename']:
                    with open(filename, 'r') as f:
                        fr = f.read()
                        if text == fr:
                            pass
                        else:
                            app.terminate()
                            reStart(filename)
                            newlist = [getVersion(), filename]
                            for i in command.split(' '):
                                newlist.append(i)
                            app = subprocess.Popen(newlist)
                            text = fr
                        f.close()
                else:
                    stopText(filename)
                    app.terminate()
                    break
        except:
            app.terminate()
            stopText(filename)

    else:
        print(f'{colorama.Fore.RED}{text}')

@app.command()
def stopAll():
    jdata = readPymon()
    jdata['filename'] = []
    writePymon(jdata)

@app.command()
def stop(filename):
    jdata = readPymon()
    res = delvalue(jdata['filename'], filename)
    if res != 'This file is not valid !':
        jdata['filename'] = res
        writePymon(jdata)
    else:
        print(f'{colorama.Fore.RED}{res}')

if __name__ == '__main__':
    app()
