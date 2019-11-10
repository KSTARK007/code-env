echo "Uninstall old versions"
echo

sudo apt-get remove docker docker-engine docker.io containerd runc

echo
echo
echo
echo
echo "uninstalled"
echo
echo
echo

sudo apt-get update

echo
echo
echo
echo
echo " Install packages to allow apt to use a repository over HTTPS:"
echo
echo
echo

sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

echo
echo
echo
echo

echo "Add Docker’s official GPG key"

echo
echo
echo
echo

echo "install curl and "

sudo apt-get -y install curl

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

echo
echo
echo
echo
echo "set up the stable repository."
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

echo
echo
echo
echo
echo "INSTALL DOCKER ENGINE - COMMUNITY"
echo
echo
echo
echo
sudo apt-get update
echo
echo
echo
echo
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
echo
echo
echo
echo
sudo docker run hello-world
echo "install successful" 
