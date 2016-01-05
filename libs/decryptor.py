from sys import argv
from zipfile import ZipFile

class Decrypt:
    dbg = False
    p_key = None
    in_file_name = None
    def __init__(self, dbg=False):
        self.setDebugFlag(dbg)
    def debug(self, debugMessage):
        if self.dbg:
            print("DEBUG: {0}".format(debugMessage))
    def setDebugFlag(self, debug):
        self.dbg = debug
    def setInputFileName(self, input_file):
        self.input_file_name = input_file
    def setEncryptionPrivateKey(self, private_key):
        self.debug("Private Key: {0}".format(private_key))
        try:
            self.p_key = open(private_key, "r").read().strip().split("\t")
            for i in xrange(len(self.p_key)):
                self.p_key[i] = int(self.p_key[i])
            return True
        except:
            return False
    def exportDecryptedData(self, output_file_name):
        """Decryption Starts Here"""
        try:
            data_ = bytearray(open(self.input_file_name, "rb").read())
            self.p_key.reverse()
            for i in xrange(len(self.p_key)):
                if data_[-1] == self.p_key[i]:
                    data_.pop(-1)
                else:
                    return False
            data_.pop(0)
            data_.reverse()
            open(output_file_name, "wb").write(data_)
            return True
        except:
            return False
def error(errMessage, exitCode=1):
    from sys import exit
    print("ERROR: {0}".format(errMessage))
    exit(exitCode)
def getCommainLineTokens(argv):
    in_data, out_file_name, p_key_name, debug = [], None, None, False
    for arg in argv:
        if arg.startswith("--in=") or arg.startswith("--input-file="):
            in_data = arg.strip().split("=")[-1]
            if in_data == "":
                error("No files to encrypt")
        elif arg.startswith("--out=") or arg.startswith("--output-file="):
            out_file_name = arg.strip().split("=")[-1]
            if out_file_name == "":
                error("Output file name can't be empty string")
        elif arg.startswith("--key=") or arg.startswith("--private-key="):
            p_key_name = arg.strip().split("=")[-1]
            if p_key_name == "":
                error("Private key name not provided")
        elif arg.startswith("--debug="):
            debug = arg.strip().split("=")[-1]
            if debug == "true" or debug == "True" or debug == "false" or debug == "False":
                debug = bool(debug)
            else:
                error("'{0}' Invalid debug flag".format(debug))
        else:
            error("Unrecognized Program Option '{0}'".format(arg))
    if in_data == None:
        error("No input file list was provided")
    if out_file_name == None:
        out_file_name = "{0}zip".format(in_data[0:-3])
    if p_key_name == None:
        error("No private key file was specified")
    return p_key_name, in_data, out_file_name, debug

def main(argv):
    from os import path
    isfile = lambda f_path: path.isfile(f_path)
    key_, in_, out_, debug_ = getCommainLineTokens(argv)
    if not isfile(in_):
        error("'{0}' Invalid Input File Path".format(argv))
    if not isfile(key_):
        error("'{0}' Not a Valid File Path".format(key_))
    if isfile(out_):
        error("Selected Output File '{0}' Already Exists".format(out_))
    dec = Decrypt(debug_)
    if not dec.setEncryptionPrivateKey(key_):
        error("Private Key File is Currepted")
    dec.setInputFileName(in_)
    if not dec.exportDecryptedData(out_):
        error("Failed to export data")
if __name__ == '__main__':
    argv.pop(0)
    main(argv)
    