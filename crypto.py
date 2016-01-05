#!/usr/bin/python

from sys import argv, exit
from os import path
from random import randint
from libs.keygen import Keygen
from libs.encryptor import Encrypt
from libs.decryptor import Decrypt

def createPrimaryKey(argv):
    keygen = Keygen()
    key_name, key_complexity = "my private key.pk", 10
    for arg in argv:
        arg = arg.strip()
        if arg.startswith("--out=") or arg.startswith("--output-file="):
            key_name = arg.split("=")[-1]
            if key_name == "":
                return False, "Private Key output file name can't be represented as an empty string"
            elif not key_name.lower().endswith(".pk"):
                key_name = "{0}.pk".format(key_name)
        elif arg.startswith("--enc=") or arg.startswith("--encryption=complexity="):
            try:
                key_complexity = int(arg.split("=")[-1])
            except:
                return False, "Invalid key complexity value was provided.Expected an integer."
        else:
            return False, "Unrecognized argument: {0}".format(arg)
    p_key = keygen.generatePrivateKey(key_complexity)
    if keygen.exportPrivateKey(p_key, key_name):
        return True, "Private key '{0}' has been created successfully with a {1}-degree complexity".format(key_name, key_complexity)
    else:
        return False, "Failed to create private key"

def encrytData(argv):
    in_, out_, pkey_ = None, None, None
    for arg in argv:
        if arg.startswith("--in=[")  and arg.endswith("]") or arg.startswith("--input-file=[") and arg.endswith("]"):
            in_ = arg.split("=")[-1][1:-1].split("?")
            if len(in_) == 1 and in_[0] == "":
                return False, "Can't encrypt an empty list of files"
            for file_ in in_:
                if not path.isfile(file_):
                    return False, "'{0}' is not a valid file path".format(file_)
        elif arg.startswith("--out=") or arg.startswith("--output-file="):
            out_ = arg.split("=")[-1].strip()
            if out_ == "":
                return False, "No output file name specified"
        elif arg.startswith("--key=") or arg.startswith("--encryption-key="):
            pkey_ = arg.split("=")[-1]
            if pkey_ == "":
                return False, "No private key file name specified"
            elif not path.isfile(pkey_):
                return False, "'{0} is not a valid private key file path'".format(pkey_)
        else:
            return False, "Unregoznied Argument: {0}".format(arg)
    if in_ == None:
        return False, "You need to specify a list of input files using--in=[file1;file2;file3;fileN]"
    if out_ == None:
        out_ = "encrypted_data"
    if pkey_ == None:
        return False, "You need to specify a private key. If you don't have one already, run crypto keygen"
    encryptor = Encrypt()
    if not encryptor.setEncryptionPrivateKey(pkey_):
        return False, "Private Key File is Currepted"
    encryptor.setInputFileList(in_)
    if not encryptor.exportEncryptedData(out_):
        return False, "Failed to export encrypted data"
    return True, "Data ecrypted into '{0}.enc' successfully".format(out_)


def crackEncryptedData(argv):
    pass

def main(argv):
    status, result = None, None
    arg = argv.pop(0).lower()
    if arg == "keygen":
        status, result = createPrimaryKey(argv)
    elif arg == "encrypt":
        status, result = encrytData(argv)
    elif arg == "decrypt":
        status, result = decryptData(argv)
    elif arg == "crack":
        status, result = crackEncryptedData(argv)
    else:
        status, result = False, "Invalid argument: {0}".format(arg)
    print("{0}".format(result))
    return status

def usage(prog_name):
    usage_info = "USAGE: \n"
    usage_info += "\t{0} keygen --out=<Private Key Output File Path> --enc=<Encryption Complexity>\n".format(prog_name)
    usage_info += "\t{0} encrypt --key=<Private Key File Path> --in=[?-seperated list of files to encrypt]\n".format(prog_name)
    usage_info += "\t{0} decrypt --key=<Private Key File Path> --in=<Encryted File Path>\n".format(prog_name)
    # more to go
    usage_info += "\tExamples: {0} keygen --out=my_key.pk --enc={1}\n".format(prog_name, randint(0, 100))
    #more to go
    return usage_info

if __name__ == '__main__':
    if len(argv) == 1:
        print("{0}".format(usage(argv[0].split("/")[-1])))
        exit(0)
    else:
        exit(main(argv[1:]))
        