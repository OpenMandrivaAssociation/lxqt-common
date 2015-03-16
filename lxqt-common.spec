%define git 0

Name: lxqt-common
Version: 0.9.1
%if %git
Release: 0.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 14
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
%endif
Summary: Common files for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
Patch0: lxqt-common-0.8.0-omv-settings.patch
Patch1: lxqt-common-0.9.1-fix-path-lxqt-policykit-agent.patch
Patch2: lxqt-common-0.8.0-startlxqt-omv-user-settings.patch
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: cmake(lxqt)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: desktop-file-utils
BuildRequires: desktop-common-data
BuildArch: noarch
Requires: xdg-user-dirs
# workaround for missing icons in desktop files on lxqt desktop
Requires: sed
Requires: openbox
Requires: desktop-common-data
Requires: distro-theme-OpenMandriva
Requires: lxmenu-data

%description
Common files for the LXQt desktop.

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%apply_patches

%cmake_qt5

%build
%make -C build

%install
%makeinstall_std -C build

mkdir -p %{buildroot}%{_datadir}/apps/kdm/sessions
cat >%{buildroot}%{_datadir}/apps/kdm/sessions/02lxqt.desktop <<'EOF'
[Desktop Entry]
Encoding=UTF-8
Name=LXQt
Comment=LXQt
TryExec=/usr/bin/startlxqt
Exec=LXQt
Icon=
Type=Application
DesktopNames=LXQt
EOF

desktop-file-validate %{buildroot}/%{_datadir}/xsessions/lxqt.desktop

# (tpg) openmandriva icons
for i in `ls -1 %{buildroot}/usr/share/lxqt/themes`; do
    ln -sf %{_iconsdir}/openmandriva.svg %{buildroot}%{_datadir}/lxqt/themes/$i/openmandriva.svg
    sed -i -e "s/mainmenu.svg/openmandriva.svg/g" %{buildroot}%{_datadir}/lxqt/themes/$i/lxqt-panel.qss
    sed -i 's|file=.*$|file=default.png|' %{buildroot}%{_datadir}/lxqt/themes/$i/wallpaper.cfg
    ln -sf %{_datadir}/mdk/backgrounds/default.png %{buildroot}%{_datadir}/lxqt/themes/$i/default.png
done

%files
%dir %{_datadir}/lxqt/openbox
%dir %{_sysconfdir}/xdg/lxqt
%dir %{_sysconfdir}/xdg/pcmanfm-qt/lxqt
%{_sysconfdir}/xdg/lxqt/*.conf
%{_sysconfdir}/xdg/pcmanfm-qt/lxqt/*.conf
%{_sysconfdir}/xdg/autostart/lxqt*
%{_sysconfdir}/xdg/menus/lxqt-applications.menu
%{_bindir}/startlxqt
%{_datadir}/lxqt/themes
%{_datadir}/apps/kdm/sessions/lxqt.desktop
%{_datadir}/lxqt/graphics
%{_datadir}/lxqt/openbox/menu.xml
%{_datadir}/lxqt/openbox/rc.xml.in
%{_datadir}/xsessions/lxqt.desktop
%{_datadir}/apps/kdm/sessions/02lxqt.desktop
%{_datadir}/desktop-directories/lxqt-*.directory
%{_iconsdir}/hicolor/scalable/places/start-here-lxqt.svg
