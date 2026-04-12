# Install

```bash
sudo apt-get -y install git

git clone --depth 1 https://github.com/Profzzor/Autoinstaller.git && cd Autoinstaller.git

bash install.sh
```

## After Reboot

### Set Wallpaper (pywal)
```bash
XDG_SESSION_TYPE=x11 wal -i ~/Pictures/overgrown-green-staircase-forest.jpg
```
### Audio and Mic
```bash
alsamixer 
```
- Press `F6` → select your sound card  
- Use arrow keys to adjust volume  
- Press `M` to unmute (MM → OO)

Test Audio (Left / Right)
```bash
speaker-test -c 2 -t wav -l 2
```
