#! /usr/bin/env python3

import os, sys, re

pid = os.getpid()
os.environ['PS1'] = '$ ' #os.getcwd()
looping = True

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())

elif rc == 0:
    while looping:
        command = input(os.environ['PS1'])
        args = re.split(' ', command)
        symbol = re.search(r'([<>\|]){1}', command)

        if command == ' ':
            continue
        elif args[0] == 'exit':
            looping = False
        elif args[0] == 'cd':
            try:
                os.chdir('{0}/{1}'.format(os.getcwd(),args[1]))
                os.write(1,('changing directory to: %s\n' % os.getcwd()).encode())
            except FileNotFoundError:
                os.write(2,('directory %s not found.\n' %args[1]).encode())
        elif args[0] == 'PS1':
            print('PS1 variable accesses!')
            os.environ['PS1'] = args[1]

        elif symbol:
            os.close(1)
            if symbol.group(1) == '>':
                sys.stdout = open(args[3], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, true)
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir,args[0])
                    try: 
                        os.execve(program, args, os.environ)
                    except FileNotFoundError: 
                        pass
                os.write(2,("It was an error running %s\n" % program).encode())

            elif symbol.group(1) == '<':
                sys.stdout = open(args[0], "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)

                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir,args[2]) 
                    try: 
                        os.execve(program, args, os.environ)
                    except FileNotFoundError:
                        pass
                os.write(2,("It was an error running %s\n" % program).encode())

            elif symbol.group(1) == '|':
                print ('piping\n')
                pr,pw = os.pipe()
                for f in (pr, pw):
                    os.set_inheritable(f, True)
                rc2 = os.fork()
                if rc2 < 0:
                    os.write(2, ("fork failed, returning %d\n" % rc).encode())

                    continue
                
                elif rc2 == 0:
                    os.close(1)
                    os.dup(pw)
                    for fd in (pr,pw):
                        os.clode(fd)

                    for dir in re.split(":", os.environ['PATH']):
                        program = "%s/%s" % (dir, args[3])
                        try:
                            os.execve(program, args, os.environ)
                        except FileNotFoundError:
                            pass
                    os.write(2,("It was an error running %s\n" % program).encode())

else:

    else: 
        os.close(0)
        os.dup(pr)
        for fd in (pw,pr):
        os.close(fd)

        else:
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass
            os.write(2,("It was an error running %s\n" % program).encode())
else:
    childPidCode = os.wait()
    os.write(1, ("Parent: My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())
