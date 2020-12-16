# procurements-scraper
TEMPORARY REPO - Written by Gaurav Godhwani, plus modifications

## Install GeckoDriver

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
export PATH=$PATH:~/bin
```

