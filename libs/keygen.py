from random import randint

class Keygen(object):
    def __init__(self):
        pass
    def generatePrivateKey(self, key_size=10):
        key = ""
        rand = lambda: randint(0, 100)
        for i in xrange(key_size):
            key += "{0}\t".format(rand())
        return key.strip()
    def exportPrivateKey(self, private_key, key_file_name = "my private key.pk"):
        open(key_file_name, "w").write(private_key)
        return True
    
def error(errMessage, exitCode=1):
    from sys import exit
    print("ERROR: {0}".format(errMessage))
    exit(exitCode)
def getCommandLineTokens(argv):
    key_name, key_size = "my private key.pk", 10
    for arg in argv:
        if arg.startswith("--out=") or arg.startswith("--output-file="):
            key_name = arg.strip().split("=")[-1]
            if key_name == "":
                error("Private Key File Name can't be empty string")
            elif not key_name.endswith(".pk"):
                key_name += ".pk"
        elif arg.startswith("--size=") or arg.startswith("--private-key-size="):
            try:
                key_size = int(arg.strip().split("=")[-1])
            except:
                error("Invalid private key size argument")
        else:
            error("Invalid Program Argument '{0}'".format(arg))
    return key_name, key_size
def main(argv):
    keygen = Keygen()
    k_name, k_size = getCommandLineTokens(argv)
    keygen.exportPrivateKey(keygen.generatePrivateKey(k_size), k_name)
if __name__ == '__main__':
    from sys import argv
    argv.pop(0)
    main(argv)
