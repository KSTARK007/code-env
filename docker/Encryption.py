# sys arg 1 = E for encryption and D - Decryption
# sys arg 2 (optional) with E = if filename mentioned then encrypt it only else encrypt all the files.
# sys arg 2 with D = filename with Secured prepended.

from Crypto.Hash import MD5
from Crypto.Cipher import AES
import os, random, sys
 
def encrypt(key, filename):
        chunksize = 128 * 1024
        outFile = os.path.join(os.path.dirname(filename), "Secured"+os.path.basename(filename))
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = ''
 
        for i in range(16):
                IV +=  chr(random.randint(0, 0xFF))
       
        encryptor = AES.new(key, AES.MODE_CBC, IV)
 
        with open(filename, "rb") as infile:
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
        outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[7:]))
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
 
print ""
try:
    choice = sys.argv[1]
except Exception as e:
    print("1st Arg is E or D")
    print("2nd Arg is file name for Encryption or Decryption")
    sys.exit(0)
print ""
password = "randomsentence"
 
encFiles = allfiles()
 
if choice == "E":
        print ""
        subchoice = "N"
        if(not(len(sys.argv) == 3)):
        	subchoice = "Y"
        if subchoice == "Y":
          for Tfiles in encFiles:
                if os.path.basename(Tfiles).startswith("Secured"):
                        print "%s is already encrypted" %str(Tfiles)
                        pass
 
                elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
                        pass
                else:
                        encrypt(MD5.new(password).digest(), str(Tfiles))
                        print "Done Encryption %s" %str(Tfiles)
                        #os.remove(Tfiles)
        else:
            print ""
            filename = sys.argv[2]
            if not os.path.exists(filename):
                print "Given file does not exist"
                sys.exit(0)
            elif filename.startswith("Secured"):
                print "%s was already encrypted" %filename
                sys.exit()
            else:
                encrypt(MD5.new(password).digest(), filename)
                print "Done Encryption %s" %filename
                #os.remove(filename)
             
elif choice == "D":
        if(not(len(sys.argv) == 3)):
            print("enter the encrypted filename with Secured prepended")
            sys.exit(0)
        print ""
        filename = sys.argv[2]
        if not os.path.exists(filename):
            print "Given file does not exist"
            sys.exit(0)
        elif not filename.startswith("Secured"):
            print "%s is was never encrypted" %filename
            sys.exit()
        else:
            decrypt(MD5.new(password).digest(), filename)
            print "Done Decryption %s" %filename
            os.remove(filename)

else:
        print ""
        print "Please choose a valid command. Either E or D as first argument"
        sys.exit()
