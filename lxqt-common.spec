Name: lxqt-common
Version: 0.7.0
Release: 1
Source0: http://lxqt.org/downloads/lxqt/%{version}/%{name}-%{version}.tar.xz
Summary: Common files for the LXQt desktop
URL: http://lxqt.org/
License: GPL
Group: Graphical desktop/KDE
BuildRequires: cmake
BuildRequires: cmake(lxqt)
BuildRequires: qt4-devel
BuildArch: noarch

%description
Common files for the LXQt desktop

%prep
%setup -q -c %{name}-%{version}
%cmake

%build
%make -C build

%install
%makeinstall_std -C build

%files
%{_datadir}/lxqt/themes
%{_sysconfdir}/lxqt
%{_sysconfdir}/pcmanfm-qt
%{_sysconfdir}/xdg/autostart/lxqt*
%{_bindir}/startlxqt
%{_datadir}/apps/kdm/sessions/lxqt.desktop
%{_datadir}/lxqt/graphics
%{_datadir}/lxqt/openbox
%{_datadir}/xsessions/lxqt.desktop
