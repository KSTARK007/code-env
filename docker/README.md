# Core Part
To be done.

# Docker usage 
- Building the docker `sudo docker image build -t test:1.0 .`
- runing an intractive docker `sudo docker run -i -t test:1.0`

# Encryption part
All the files are encrypted and decrypted, using a symmetric cipher using AES and hased using MD5.

Operating system interface and System specific parameters were used accordingly. 
## Prerequisite:
- `pip install pycrypto` 
## Usage:
- 1st argument : E for encryption and D for Decryption
- 2nd argument with E (optional) :  If filename mentioned then encrypt it else encrypt all the files in the current dir.

example:

` python main.py E test.txt` 

output - Securedtest.txt 


` python main.py E`

All files in the dir are encrypted with `Secured` keyword prepended.

- 2nd argument with D : filename with `Secured` keyword prepended.

example:

`python main.py D Securedtest.txt`

output - test.txt
## Important:

- Save and Run the code in a seperate directory. It should not effect our work flow. 

- key should be defined in the file itself.
- User inputed key is MD5 hashed and then used as the key for AES encryption. 
- In this script, the code is devised for the single encryption and single decryption.
