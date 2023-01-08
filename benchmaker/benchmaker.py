#!/usr/bin/env python3
import argparse
import io
import json
import os
import platform
import signal
import subprocess
import sys
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Tool to create a benchmark json file. \n\
        It launch N times the command and calculates de average.\n\
        The benchmark should print a single number during the execution corresponding to the unit (default milliseconds)')
parser.add_argument("filename", type=str, help="Path of json result file")

parser.add_argument("-v","--verbose", help="increase output verbosity", action='store_true')

args = parser.parse_args()
args.filename = args.filename if args.filename.endswith('.json') else args.filename+'.json'
def signal_handler(sig, frame):
    print(' Exiting gracefully')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
def print_if_verbose(*a, **aa):
    if args.verbose:
        print(*a, **aa)

def clear(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 
def askInput():
    print('> ', end='')
    return input()

def loadFileIfExists():
    def loadInSargs(result):
        if result.get('DESCRIPTION'):
            sargs['description'] = result['DESCRIPTION']
        if result.get('VALUE'):
            sargs['unit'] = result['VALUE']
        if result.get('RANGE'):
            sargs['range'] = result['RANGE']
        if not result.get('TESTS'):
            return
        sargs['tests'] = [t for t in result['TESTS']]
        firstTest =next(iter(result['TESTS'].values()))
        sargs['version'] = firstTest['version']
        sargs['numberoftests'] = firstTest['numberoftests']

    if not os.path.exists(args.filename):
        return 'New benchmark: '+args.filename
    with open(args.filename, 'r') as f:
        js = json.load(f)
        loadInSargs(js)
    return 'Loaded existing file, found tests: '+ ' | '.join(i for i in sargs['tests'])

def askNumberOfTests():
    print('Number of time the test will be executed in order to make an average:')
    n = None
    while n == None:
        a = askInput()
        try:
            n = int(a)
        except:
            return print('type not recognized as int, please try again:')
    sargs['numberoftests'] = n

def askRange():
    print('3 values that will generate the number that will be passed to your program')
    print('min max step: so for example 0 10 2 will send [0 2 4 6 8 10] (single 0 means no range)')
    isok = False
    while not isok:
        b = askInput().split(' ')
        if len(b) == 3:
            if all(i.isnumeric for i in b):
                sargs['range'] = [int(i) for i in b]
                isok = True
        elif len(b) == 1 and b[0] == '0':
            sargs['range'] = [0]
            isok = True


def askNameOfTest():
    print('Name of this test:')
    a = askInput()
    sargs['name'] = a
def askVersion():
    print('Versions of the libraries, language ...:')
    sargs['version'] = askInput()
def askCommand():
    print('run the test using:')
    sargs['command'] = askInput()
def askValue():
    print('what is the program printing (default milliseconds):')
    a = askInput()
    sargs['unit'] = a if a != '' else 'milliseconds'
def askLanguage():
    print('what is the language used:')
    sargs['language'] = askInput()
def askCode():
    print('Paste the important part of the code used in this test then type: done!')
    a = []
    while a == [] or a[-1].lower() != 'done!':
        a.append(input())
    sargs['code'] = '\n'.join(a[:-1])
def askDescription():
    print('Description:')
    sargs['description'] = askInput()
def printCurrentArgs():
    clear()
    m = max(map(len, table.keys()))
    i = 1
    for key in table.keys():
        if key not in sargs.keys():
            continue
        print(str(i)+':',key, end= '')
        dif = m - len(key)

        print(' '*dif, end= ' ')

        if not sargs[key] and key in optional:
            print('[~]', end=' ')
        elif not sargs[key]:
            print('[ ]', end=' ')
        else:
            print('[X]', end=' ')
        if isinstance(sargs[key], list):
            print(*sargs[key], end='')
        elif isinstance(sargs[key], str):
            print(sargs[key].split('\n')[0][:40], end='')
        else:
            print(sargs[key], end='')
        print()
        i += 1
def canrun():
    for key in sargs.keys():
        if key in optional:
            continue
        elif not sargs[key]:
            return False
    return True
def whatValues():
    l = []
    for key in sargs.keys():
        if key in optional:
            continue
        elif not sargs[key]:
            l.append(key)
    return l
def reset():
    li = ['code', 'name']
    for i in li:
        sargs[i] = ''

def ls():    
    return 'Tests in '+args.filename+': ' + ' | '.join(t for t in sargs['tests'])

def doTheTest():
    average = 0
    def doNTest(p=None):
        results = []
        for i in range(sargs['numberoftests']):
            output = None
            command = sargs['command'].split(' ')
            if p is not None:
                command += [str(p)]
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            try:
                float(output)
            except:
                raise Exception('Your command did not return a valid number:' + str(output))
            results.append(float(output))
            print(command[-1], end=' ')
            print(i, end=' ', flush=True)
            print_if_verbose(': ', results[-1]*1000, sargs['unit'])
        print_if_verbose(sargs['numberoftests'], ' tests')
        print(' FINISHED!')
        average = round(sum(results)/ len(results), 3) 
        return average
    print('Running...')
    rangeArg = sargs['range']
    if len(rangeArg) == 3:
        sargs['LABELS'] = list(range(rangeArg[0], rangeArg[1]+1, rangeArg[2]))
        average = [doNTest(step) for step in sargs['LABELS']]
    else:
        average = doNTest()
    

    result = {}
    result['TESTS'] = {}
    if os.path.exists(args.filename):
        print_if_verbose('json file not found, creating a new one called: ', args.filename)
        with open (args.filename, 'r') as f:
            result = json.load(f)
    print_if_verbose('found an existing json file called: ', args.filename)

    result['TESTS'][sargs['name']] = {'average': average, 'version': sargs['version'], 'numberoftests': sargs['numberoftests'], 'code': sargs['code']}
    if not result.get('CPU'):
        result['CPU'] = platform.processor()
    if sargs['unit'] or not result.get('VALUE'):
        result['VALUE'] = sargs['unit']
    if sargs['description'] or not result.get('DESCRIPTION'):
        result['DESCRIPTION'] = sargs['description']
    result['RANGE'] = sargs['range']
    print_if_verbose('saving in: ', args.filename)
    with open(args.filename, 'w') as f:
        json.dump(result, f, indent=4)
    sargs['tests'].append(sargs['name'])
    return ' '.join(['saved', sargs['name'], 'in', args.filename])

def run():
    if canrun():
        try:
            a = doTheTest()            
        except Exception as e:
            return str(e)
        reset()
        return a
    else:
        
        return('values that must be set:' + ','.join(whatValues()))

def myhelp():
    return '\n\
        Type a number or the name of a field then press enter to set its value.\n\
        [X] = value set\n\
        [~] = optional value not set\n\
        [ ] = value that need to be set\n\
        \n\
        Commands:\n\
        \n\
        run = run the current test\n\
        ls = list tests in json file\n\
        rm = remove a test\n\
        stop = stop the program\n\
        help = show the program\'s helper'

def rm():
    print('Test to delete:', ' | '.join(t for t in sargs['tests']))
    a = askInput()
    if a in sargs['tests']:
        save = {}
        with open(args.filename, 'r') as f:
            save = json.load(f)
            if a not in save['TESTS']:
                return 'Nothing deleted, '+a+' not found in ' + args.filename
            save['TESTS'].pop(a , None)
        with open(args.filename, 'w') as f:
            json.dump(save, f, indent=4)
        sargs['tests'].remove(a)
        return 'Test '+a+' successfully deleted'
    else:
        return 'Nothing deleted, '+a+' not found'

def stop():
    print('Exiting gracefully')

def isACommand(s):
    if s == '':
        return 'Command not found'
    keys = list(table.keys())
    if s.isnumeric() and 1 <= int(s) <= len(keys) +1:
        return table[keys[int(s)-1]]()
    for i in keys:
        if i.startswith(s):
            return table[i]()
    return 'Command not found'

table = OrderedDict([
    ('name', askNameOfTest),
    ('command', askCommand),
    ('description', askDescription),
    ('code', askCode),
    ('version', askVersion),
    ('numberoftests', askNumberOfTests),
    ('range', askRange),
    ('unit', askValue),
    ('ls', ls),
    ('run', run),
    ('help', myhelp),
    ('rm', rm),
    ('stop', stop)
])
optional = ['description', 'code', 'version', 'numberoftests', 'range', 'tests']
sargs = OrderedDict([
            ('name', ''),
            ('command', ''),
            ('unit', 'milliseconds'),
            ('numberoftests', 10),
            ('range', [0]),
            ('description', ''),
            ('code', ''),
            ('version', ''),
            ('tests', [])
        ])
c = ''
commandOutput = loadFileIfExists()
while c != 'stop':
    printCurrentArgs()
    if commandOutput:
        print(commandOutput)       

    if canrun():
        print('You can now run the test using: run')
    c = askInput()
    commandOutput = isACommand(c)

