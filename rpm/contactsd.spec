Name: contactsd
Version: 1.3.4
Release: 1
Summary: Telepathy <> QtContacts bridge for contacts
Group: System/Libraries
URL: https://git.merproject.org/mer-core/contactsd
License: LGPLv2.1+ and (LGPLv2.1 or LGPLv2.1 with Nokia Qt LGPL Exception v1.1)
Source0: %{name}-%{version}.tar.bz2
Requires: systemd
Requires: systemd-user-session-targets
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(TelepathyQt5)
BuildRequires: pkgconfig(Qt5Contacts)
BuildRequires: pkgconfig(Qt5Versit)
# mlite required only for tests
BuildRequires: pkgconfig(mlite5)
BuildRequires: pkgconfig(mlocale5)
BuildRequires: pkgconfig(libmkcal-qt5)
BuildRequires: pkgconfig(libkcalcoren-qt5)
BuildRequires: pkgconfig(telepathy-glib)
BuildRequires: pkgconfig(qofono-qt5)
BuildRequires: pkgconfig(qofonoext)
BuildRequires: pkgconfig(qtcontacts-sqlite-qt5-extensions) >= 0.1.64
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(gio-2.0)
# pkgconfig(buteosyncfw5) is not correctly versioned, use the provider package instead:
#BuildRequires: pkgconfig(buteosyncfw5) >= 0.6.33
BuildRequires: buteo-syncfw-qt5-devel >= 0.6.33
BuildRequires: pkgconfig(qt5-boostable)
BuildRequires: qt5-qttools
BuildRequires: qt5-qttools-linguist
Requires: libqofono-qt5 >= 0.67
Requires: mapplauncherd-qt5

%description
contactsd is a service for collecting and observing changes in roster list
from all the users telepathy accounts (buddies, their status and presence
information), and store it to QtContacts.

%files
%defattr(-,root,root,-)
%{_libdir}/systemd/user/contactsd.service
%{_libdir}/systemd/user/post-user-session.target.wants/contactsd.service
%{_bindir}/contactsd
%{_libdir}/contactsd-1.0/plugins/*.so
%{_datadir}/translations/contactsd.qm
%{_datadir}/translations/contactsd_eng_en.qm
# we currently don't have a backup framework
%exclude /usr/share/backup-framework/applications/contactsd.conf


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{_includedir}/contactsd-1.0/*
%dir %{_includedir}/contactsd-1.0
%{_libdir}/pkgconfig/*.pc


%package tests
Summary: Tests for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: blts-tools

%description tests
%{summary}.

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}

%package ts-devel
Summary: Translation source for contactsd
Group: System/Applications

%description ts-devel
Translation source for contactsd

%files ts-devel
%defattr(-,root,root,-)
%{_datadir}/translations/source/contactsd.ts


%prep
%setup -q -n %{name}-%{version}

%build
export QT_SELECT=5
export VERSION=%{version}
./configure --bindir %{_bindir} --libdir %{_libdir} --includedir %{_includedir}
%qmake5
make %{?_smp_mflags}


%install
%qmake5_install

mkdir -p %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants
ln -s ../contactsd.service %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants/

%post
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user try-restart contactsd.service || :
fi

%postun
if [ "$1" -eq 0 ]; then
systemctl-user stop contactsd.service || :
systemctl-user daemon-reload || :
fi

