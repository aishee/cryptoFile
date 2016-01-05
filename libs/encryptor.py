from sys import argv
from zipfile import ZipFile

class Encrypt:
    dbg = False
    in_data = []
    p_key = None
    out_file_name = None
    def __init__(self, dbg = False):
        self.setDebugFlag(dbg)
    def debug(self, debugMessage):
        if self.dbg:
            print("DEBUG: {0}".format(debugMessage))
    def setDebugFlag(self, debug):
        self.dbg = debug
    def setInputFileList(self, input_file_list):
        self.in_data = []
        self.debug("Adding the following files to encryption list")
        for item in input_file_list:
            self.debug("{0}".format(item))
            self.in_data.append(item)
    def setEncryptionPrivateKey(self, private_key):
        self.debug("Private Key: {0}".format(private_key))
        try:
            self.p_key = open(private_key, "r").read().strip().split("\t")
            for i in xrange(len(self.p_key)):
                self.p_key[i] = int(self.p_key[i])
            return True
        except:
            return False
    def exportEncryptedData(self, output_file_name):
        from os import remove
        out = "{0}.zip".format(output_file_name)
        self.debug("Output file name: {0}".format(out))
        try:
            """ Add all file to a zip file"""
            zipped_data = ZipFile(out, "w")
            self.debug("Adding the following files to {0}".format(out))
            for item in self.in_data:
                self.debug("{0}".format(item))
                zipped_data.write(item)
            zipped_data.close()
            """Encryption Starts Here"""
            self.debug("Now encrypting data")
            data_ = bytearray(open(out, "rb").read())
            data_.reverse()
            data_.insert(0, len(self.p_key))
            for key_value in self.p_key:
                data_.append(key_value)
            out2 = out.replace("zip", "enc")
            open(out2, "wb").write(data_)
            remove(out)
            return True
        except:
            return False        
               
def error(errMessage, exitCode = 1):
    from sys import exit
    print("ERROR: {0}".format(errMessage))
    exit(exitCode)
def getCommandLineTokens(argv):
    in_data, out_file_name, p_key_name, debug = [], None, None, False
    for arg in argv:
        if arg.startswith("--in=[") and arg.endswith("]") or arg.startswith("--input-file=[") and arg.endswith("]"):
            in_data = arg.strip().split("=")[-1][1:-1].split("?")
            if in_data == [""]:
                error("No files to encrypt")
        elif arg.startswith("--out=") or arg.startswith("--out-file="):
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
    if in_data == []:
        error("No input file list was provided")
    if out_file_name == None:
        error("No output file provided")
    if p_key_name == None:
        error("No private key file was specified")
    return p_key_name, in_data, out_file_name, debug

def main(argv):
    from os import path
    isfile = lambda f_path: path.isfile(f_path)
    key_, in_, out_,debug_ = getCommandLineTokens(argv)
    for file_name in in_:
        if not isfile(file_name):
            error("'{0}' Invalid Input File Path".format(file_name))
    if not isfile(key_):
        error("'{0}' Not a valid file path".format(key))
    if isfile(out_):
        error("Selected Output file '{0}' Already Exists".format(out_))
    enc = Encrypt(debug_)
    if not enc.setEncryptionPrivateKey(key_):
        error("Private Key File is Currepted")
    enc.setInputFileList(in_)
    if not enc.exportEncryptedData(out_):
        error("Failed to export data")

if __name__ == '__main__':
    argv.pop(0)
    main(argv)
