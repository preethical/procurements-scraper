# procurements-scraper
TEMPORARY REPO - Written by Gaurav Godhwani, plus modifications

## 1. Install GeckoDriver

```
mkdir ~/downloads # if necessary
mkdir ~/bin       # if necessary

### download geckodriver ###
cd ~/downloads
# modify 'v0.28.0' as necessary:
wget https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver

### install geckodriver locally ###
mv geckodriver ~/bin
echo 'export PATH=$PATH:~/bin' >> ~/.bashrc  # adjust for zsh and other shells
```

## 2. Install Python Dependencies

```
sudo apt install python3-pip  # on linux

pip3 install lxml
pip3 install selenium
```
