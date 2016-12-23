%define git 0

Name: lxqt-common
Version: 0.11.1
%if %git
Release: 1.%git.1
Source0: %{name}-%{git}.tar.xz
%else
Release: 1
Source0: https://github.com/lxde/%{name}/archive/%{name}-%{version}.tar.xz
%endif
Summary: Common files for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/Other
Patch0: lxqt-common-0.8.0-omv-settings.patch
Patch1: lxqt-common-0.9.1-fix-path-lxqt-policykit-agent.patch
Patch2: lxqt-common-0.8.0-startlxqt-omv-user-settings.patch
BuildRequires: cmake
BuildRequires: qmake5
BuildRequires: ninja
BuildRequires: cmake(lxqt)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(lxqt-build-tools)
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
Requires: menu-cache
Requires: breeze
Requires: breeze-icons

%description
Common files for the LXQt desktop.

%prep
%if %git
%setup -qn %{name}-%{git}
%else
%setup -q
%endif
%apply_patches

%cmake_qt5 -G Ninja

%build
# Need to be in a UTF-8 locale so grep (used by the desktop file
# translation generator) doesn't scream about translations containing
# "binary" (non-ascii) characters
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
%ninja -C build

%install
# Need to be in a UTF-8 locale so grep (used by the desktop file
# translation generator) doesn't scream about translations containing
# "binary" (non-ascii) characters
export LANG=en_US.utf-8
export LC_ALL=en_US.utf-8
%ninja_install -C build

desktop-file-validate %{buildroot}/%{_datadir}/xsessions/lxqt.desktop

# (tpg) openmandriva icons
for i in `ls -1 %{buildroot}/usr/share/lxqt/themes`; do
    ln -sf %{_iconsdir}/openmandriva.svg %{buildroot}%{_datadir}/lxqt/themes/$i/openmandriva.svg
    sed -i -e "s/mainmenu.svg/openmandriva.svg/g" %{buildroot}%{_datadir}/lxqt/themes/$i/lxqt-panel.qss
    sed -i 's|file=.*$|file=default.png|' %{buildroot}%{_datadir}/lxqt/themes/$i/wallpaper.cfg ||:
    ln -sf %{_datadir}/mdk/backgrounds/default.png %{buildroot}%{_datadir}/lxqt/themes/$i/default.png
done

# (tpg) we do not have any KDM in 2015.0 or newer
rm -rf %{buildroot}%{_datadir}/kdm/sessions/lxqt.desktop

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
%{_datadir}/lxqt/graphics
%{_datadir}/lxqt/openbox/menu.xml
%{_datadir}/lxqt/openbox/rc.xml.in
%{_datadir}/xsessions/lxqt.desktop
%{_datadir}/desktop-directories/lxqt-*.directory
%{_iconsdir}/hicolor/scalable/places/start-here-lxqt.svg
