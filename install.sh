#!/bin/bash

set -euo pipefail

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y meson ninja-build pkg-config x11proto-dev xorg-dev x11proto-randr-dev xtrans-dev libpixman-1-dev libxkbcommon-x11-dev libxfont-dev libxcvt-dev 
sudo apt-get install -y libdrm-dev libepoxy-dev x11proto-present-dev libxkbfile-dev libudev-dev libxshmfence-dev libbsd-dev x11proto-xf86dri-dev libgl1-mesa-dev libglu1-mesa-dev
sudo apt-get install -y libgl-dev xutils-dev mesa-common-dev libgbm-dev libxcb-shape0-dev libxcb-util-dev libxcb-icccm4-dev autoconf automake libtool libinput-dev libx11-dev 
sudo apt-get install -y cmake libxau-dev libxext-dev libxinerama-dev libxv-dev libxrender-dev libxdmcp-dev libxcb1-dev libxshmfence-dev libpixman-1-dev libbsd-dev xbitmaps 
sudo apt-get install -y xkb-data libxfont-dev x11-xkb-utils mesa-utils libgl1-mesa-dri libgbm-dev open-vm-tools open-vm-tools-desktop fonts-font-awesome 
sudo apt-get install -y git i3-wm i3blocks xinit xterm x11-xserver-utils vim alacritty libkrb5-dev python3-dev thunar python3-pip feh imagemagick picom rofi
sudo apt-get install -y lxappearance qt5ct qt6ct arc-theme adwaita-icon-theme papirus-icon-theme flameshot

sudo apt-get remove -y vim-tiny && sudo ln -sf /usr/bin/vim /usr/bin/vi

cd /tmp && git clone --depth 1 https://github.com/X11Libre/xserver.git && cd xserver

meson setup build --prefix=/usr/local --localstatedir=/var --sysconfdir=/etc/X11 --buildtype=release -Dxnest=false -Dxvfb=false

ninja -C build

sudo ninja -C build install

export PATH="/usr/local/bin:$PATH"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/lib/x86_64-linux-gnu/pkgconfig:$PKG_CONFIG_PATH"
export ACLOCAL_PATH="/usr/share/aclocal:/usr/local/share/aclocal"

cd /tmp && git clone --depth 1 https://github.com/X11Libre/xf86-input-libinput.git && cd xf86-input-libinput

meson setup build --prefix=/usr/local

ninja -C build

sudo ninja -C build install

cd /tmp && git clone --depth 1 https://github.com/X11Libre/xf86-input-keyboard.git && cd xf86-input-keyboard

./autogen.sh --prefix=/usr/local PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/lib/x86_64-linux-gnu/pkgconfig"

make && sudo make install

cd /tmp && git clone --depth 1 https://github.com/X11Libre/xf86-input-vmmouse.git && cd xf86-input-vmmouse

./autogen.sh --prefix=/usr/local PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/lib/x86_64-linux-gnu/pkgconfig"

make && sudo make install

sudo mv /usr/bin/Xorg /usr/bin/Xorg.xorg-backup

sudo mv /usr/bin/X /usr/bin/X.xorg-backup

sudo apt remove -y xserver-xorg-core

sudo ln -sf /usr/local/bin/Xorg /usr/bin/Xorg

sudo ln -sf /usr/local/bin/Xorg /usr/bin/X

sudo chmod u+s /usr/local/bin/Xorg

cat > ~/.bash_profile <<'EOF'
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
  exec startx
fi
EOF

cat > ~/.xinitrc <<'EOF'
export QT_QPA_PLATFORMTHEME=qt5ct
exec /usr/bin/i3
EOF

cd /tmp && git clone --depth 1 https://github.com/vivien/i3blocks-contrib.git

cd i3blocks-contrib/ && sudo make install PREFIX=/usr/local

cd $(find / -type d -name Autoinstaller 2>/dev/null && echo -n 1 )

mkdir -p ~/.config/picom
cp config/picom.conf ~/.config/picom/

mkdir -p ~/.config/alacritty/
cp config/alacritty.toml ~/.config/alacritty/

pip install pywal --break-system-packages

mkdir -p ~/.config/wal
cat > ~/.config/wal/config << 'EOF' 
[backend]
backend = 'feh'
options = '--bg-fill'
EOF

mkdir -p ~/.config/autostart
cat > .config/autostart/Flameshot.desktop <<'EOF'
[Desktop Entry]
Name=flameshot
Icon=flameshot
Exec=flameshot
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF

mkdir -p ~/Pictures/
cp overgrown-green-staircase-forest.jpg ~/Pictures/

mkdir -p ~/.config/i3
cp config/config ~/.config/i3/
cp config/i3blocks.conf ~/.config/i3/
cp config/bashrc ~/.bashrc

mkdir -p ~/.config/rofi
cp config/config.rasi ~/.config/rofi/

# Clean up
cd /tmp && sudo rm -rf xf86-input-keyboard/ xf86-input-libinput/ xf86-input-vmmouse/ xserver/ i3blocks-contrib/

sudo apt autoremove -y

echo
echo "===================================================="
echo "AFTER REBOOT, RUN THIS COMMAND:"
echo
echo "XDG_SESSION_TYPE=x11 wal -i ~/Pictures/overgrown-green-staircase-forest.jpg"
echo "===================================================="
echo

sleep 5

sudo reboot
