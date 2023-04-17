#!/bin/bash


echo 'Install package for Qt GUI'


sudo dpkg -i libllvm10_1%3a10.0.0-4ubuntu1_amd64.deb
sudo dpkg -i libclang1-10_1%3a10.0.0-4ubuntu1_amd64.deb
sudo dpkg -i libdouble-conversion3_3.1.5-4ubuntu1_amd64.deb
sudo dpkg -i libpthread-stubs0-dev_0.4-1_amd64.deb
sudo dpkg -i xorg-sgml-doctools_1%3a1.11-1_all.deb
sudo dpkg -i x11proto-dev_2019.2-1ubuntu1_all.deb
sudo dpkg -i x11proto-core-dev_2019.2-1ubuntu1_all.deb
sudo dpkg -i xtrans-dev_1.4.0-1_all.deb
sudo dpkg -i libxdmcp-dev_1%3a1.1.3-0ubuntu1_amd64.deb
sudo dpkg -i libxau-dev_1%3a1.0.9-0ubuntu1_amd64.deb
sudo dpkg -i libxcb1-dev_1.14-2_amd64.deb
sudo dpkg -i libx11-dev_2%3a1.6.9-2ubuntu1.2_amd64.deb
sudo dpkg -i libglx-dev_1.3.2-1~ubuntu0.20.04.2_amd64.deb
sudo dpkg -i libgl-dev_1.3.2-1~ubuntu0.20.04.2_amd64.deb
sudo dpkg -i libegl-dev_1.3.2-1~ubuntu0.20.04.2_amd64.deb
sudo dpkg -i libglu1-mesa-dev_9.0.1-1build1_amd64.deb
sudo dpkg -i libpcre2-16-0_10.34-7ubuntu0.1_amd64.deb
sudo dpkg -i libqt5core5a_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5concurrent5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5dbus5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libxcb-xinput0_1.14-2_amd64.deb
sudo dpkg -i libxcb-xinerama0_1.14-2_amd64.deb
sudo dpkg -i libqt5network5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5gui5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5widgets5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5xml5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5designer5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5designercomponents5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qtchooser_66-2build1_amd64.deb
sudo dpkg -i qt5-qmake-bin_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i qt5-qmake_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5sql5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5sql5-sqlite_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i x11proto-xext-dev_2019.2-1ubuntu1_all.deb
sudo dpkg -i libxext-dev_2%3a1.3.4-0ubuntu1_amd64.deb
sudo dpkg -i libqt5printsupport5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5test5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libvulkan-dev_1.2.131.2-1_amd64.deb
sudo dpkg -i qtbase5-dev-tools_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i qtbase5-dev_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5help5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5opengl5_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5opengl5-dev_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i libqt5positioning5_5.12.8+dfsg-0ubuntu1_amd64.deb
sudo dpkg -i libqt5qml5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5quick5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5quickwidgets5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5sensors5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5svg5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5webchannel5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i libqt5webkit5_5.212.0~alpha4-1ubuntu2.1_amd64.deb
sudo dpkg -i qdoc-qt5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qhelpgenerator-qt5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qt5-assistant_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qt5-gtk-platformtheme_5.12.8+dfsg-0ubuntu2.1_amd64.deb
sudo dpkg -i qtattributionsscanner-qt5_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qttools5-dev-tools_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qttools5-dev_5.12.8-0ubuntu1_amd64.deb
sudo dpkg -i qttranslations5-l10n_5.12.8-0ubuntu1_all.deb


#-----------------------------------------------------------------------------------------------
# need to download this dependencies file before intallation
# use to support Qt GUI

# if have internet connection : just run this 2 command
# i)  sudo apt-get install qttools5-dev-tools
# ii) sudo apt-get install qttools5-dev
: '
sudo apt-get remove libclang1-10
sudo apt-get remove libdouble-conversion3
sudo apt-get remove libegl-dev
sudo apt-get remove libgl-dev
sudo apt-get remove libglu1-mesa-dev
sudo apt-get remove libglx-dev
sudo apt-get remove libllvm10
sudo apt-get remove libpcre2-16-0
sudo apt-get remove libpthread-stubs0-dev
sudo apt-get remove libqt5concurrent5
sudo apt-get remove libqt5core5a
sudo apt-get remove libqt5dbus5
sudo apt-get remove libqt5designer5
sudo apt-get remove libqt5designercomponents5
sudo apt-get remove libqt5gui5
sudo apt-get remove libqt5help5
sudo apt-get remove libqt5network5
sudo apt-get remove libqt5opengl5
sudo apt-get remove libqt5opengl5-dev
sudo apt-get remove libqt5positioning5
sudo apt-get remove libqt5printsupport5
sudo apt-get remove libqt5qml5
sudo apt-get remove libqt5quick5
sudo apt-get remove libqt5quickwidgets5
sudo apt-get remove libqt5sensors5
sudo apt-get remove libqt5sql5
sudo apt-get remove libqt5sql5-sqlite
sudo apt-get remove libqt5svg5
sudo apt-get remove libqt5test5
sudo apt-get remove libqt5webchannel5
sudo apt-get remove libqt5webkit5
sudo apt-get remove libqt5widgets5
sudo apt-get remove libqt5xml5
sudo apt-get remove libvulkan-dev
sudo apt-get remove libx11-dev
sudo apt-get remove libxau-dev
sudo apt-get remove libxcb-xinerama0
sudo apt-get remove libxcb-xinput0
sudo apt-get remove libxcb1-dev
sudo apt-get remove libxdmcp-dev
sudo apt-get remove libxext-dev
sudo apt-get remove qdoc-qt5
sudo apt-get remove qhelpgenerator-qt5
sudo apt-get remove qt5-assistant
sudo apt-get remove qt5-gtk-platformtheme
sudo apt-get remove qt5-qmake qt5-qmake-bin
sudo apt-get remove qtattributionsscanner-qt5
sudo apt-get remove qtbase5-dev
sudo apt-get remove qtbase5-dev-tools qtchooser
sudo apt-get remove qttools5-dev
sudo apt-get remove qttools5-dev-tools
sudo apt-get remove qttranslations5-l10n
sudo apt-get remove x11proto-core-dev
sudo apt-get remove x11proto-dev
sudo apt-get remove x11proto-xext-dev
sudo apt-get remove xorg-sgml-doctools
sudo apt-get remove xtrans-dev
'
