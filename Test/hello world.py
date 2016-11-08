from subprocess import call
a = call('echo 1', shell=True, stdin=None, stdout=None, stderr=None)
print (a)