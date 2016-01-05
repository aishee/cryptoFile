class Cracker():
    error_queue = []
    encrypted_file_name, decrypted_file_name = None, None
    enc_comp = 0
    decrypted = None
    def __init__(self, encrypted_file_name):
        self.encrypted_file_name = encrypted_file_name
        while len(self.error_queue) > 0:
            self.error_queue.pop()
    def setEncryptionComplexity(self, enc_complexity):
        self.enc_comp = enc_complexity
    def setDecryptedOutputFileName(self, output_file_name):
        self.decrypted_file_name = output_file_name
    def hasValidEncryptionComplexity(self):
        return self.enc_comp == int(bytearray(open(self.encrypted_file_name, "rb").read())[0])
    def decrypt(self):
        #try:
            data_ = bytearray(open(self.encrypted_file_name, "rb").read())
            data_.pop(0)
            for i in xrange(self.enc_comp):
                data_.pop(-1)
            data_.reverse()
            open(self.decrypted_file_name, "wb").write(data_)
            return True
        #except
def error(errMessage, exitCode=1):
    from sys import exit
    print("ERROR: {0}".format(errMessage))
    exit(exitCode)

def getCommandLineTokens(argv):
    in_, out_, pk_complexity = None, None, None
    for arg in argv:
        arg = arg.strip()
        if arg.startswith("--in=") or arg.startswith("--input-file="):
            in_ = arg.split("=")[-1]
        elif arg.startswith("--out=") or arg.startwith("--output-file="):
            out_ = arg.split("=")[-1]
        elif arg.startswith("--encryption-complexity=") or arg.startswith("--enc="):
            try:
                pk_complexity = int(arg.split("=")[-1])
            except:
                error("Invalid Encryption Complexity Provided")
        else:
            error("'{0}' Unrecognized Program Option".format(arg))
    if in_ == None or in_ == "":
        error("Encrypted File Name Not Provided")
    if out_ == None:
        out_ = "{0}zip".format(in_[0:-3])
    if pk_complexity == None:
        error("Encryption Complexity Not Provided")
    return in_,out_, pk_complexity

def main(argv):
    from os import path
    in_, out_, pk_comp = getCommandLineTokens(argv)
    if not path.isfile(in_):
        error("'Invalid File Path {0}'".format(in_))
    if path.isfile(out_):
        error("'{0}' Already Exists.".format(out_))
    cr = Cracker(in_)
    cr.setEncryptionComplexity(pk_comp)
    cr.setDecryptedOutputFileName(out_)
    if not cr.hasValidEncryptionComplexity():
        error("Invalid Encryption Complexity Provided.")
    if not cr.decrypt():
        error("Failed to Decrypt {0}".format(in_))
if __name__ == '__main__':
    from sys import argv
    argv.pop(0)
    main(argv)