# sys arg 1 = E for encryption and D - Decryption
# sys arg 2 (optional) with E = if filename mentioned then encrypt it only else encrypt all the files.
# sys arg 2 with D = filename with Secured prepended.
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import os, random, sys
 
def encrypt(key, filename):
        cmd_to_run="cp ./"+filename+" ./D"+filename
        os.system(cmd_to_run)
        chunksize = 128 * 1024
        outFile = os.path.join(os.path.dirname(filename),os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = ''
 
        for i in range(16):
                IV +=  chr(random.randint(0, 0xFF))
       
        encryptor = AES.new(key, AES.MODE_CBC, IV)
 
        with open("D"+filename, "rb") as infile:
                with open(outFile, "wb") as outfile:
                        outfile.write(filesize)
                        outfile.write(IV)
                        while True:
                                chunk = infile.read(chunksize)
                               
                                if len(chunk) == 0:
                                        break
 
                                elif len(chunk) % 16 !=0:
                                        chunk += ' ' *  (16 - (len(chunk) % 16))
 
                                outfile.write(encryptor.encrypt(chunk))
 
def decrypt(key, filename):
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename))
        chunksize = 128 * 1024
        with open(filename, "rb") as infile:
                filesize = infile.read(16)
                IV = infile.read(16)
 
                decryptor = AES.new(key, AES.MODE_CBC, IV)
               
                with open(outFile, "wb") as outfile:
                        while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                        break
 
                                outfile.write(decryptor.decrypt(chunk))
 
                        outfile.truncate(int(filesize))
       
def allfiles():
        allFiles = []
        for root, subfiles, files in os.walk(os.getcwd()):
                for names in files:
                        allFiles.append(os.path.join(root, names))
        return allFiles
 
try:
    choice = sys.argv[1]
except Exception as e:
    print("1st Arg is E or D")
    print("2nd Arg is file name for Encryption or Decryption")
    sys.exit(0)

password = "randomsentence"
 
encFiles = allfiles()
 
if choice == "E":
    filename = sys.argv[2]
    if not os.path.exists(filename):
        print ("Given file does not exist")
        sys.exit(0)
    else:
        encrypt(MD5.new(password).digest(), filename)
        print("Done Encryption %s" %filename)
        #os.remove(filename)
             
elif choice == "D":
        if(not(len(sys.argv) == 3)):
            print("enter the encrypted filename with Secured prepended")
            sys.exit(0)
        print ("")
        filename = sys.argv[2]
        if not os.path.exists(filename):
            print("Given file does not exist")
            sys.exit(0)
        else:
            decrypt(MD5.new(password).digest(), filename)
            print("Done Decryption %s" %filename)
            #os.remove(filename)

else:
        print("Please choose a valid command. Either E or D as first argument")
        sys.exit()
