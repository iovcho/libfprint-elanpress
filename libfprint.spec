Name:           libfprint
Epoch:          1
Version:        1.94.10
Release:        1.elanpress.fa2f98f%{?dist}
Summary:        Fingerprint library with the elanpress driver for ELAN 04f3:0c6e

License:        LGPL-2.1-or-later
URL:            https://github.com/filip-rs/libfprint
Source0:        libfprint-%{version}.tar.gz

BuildRequires:  meson >= 0.56.0
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  glib2-devel
BuildRequires:  libgusb-devel
BuildRequires:  pixman-devel
BuildRequires:  nss-devel
BuildRequires:  cairo-devel
BuildRequires:  libgudev-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  systemd-devel
BuildRequires:  openssl-devel
BuildRequires:  python3

Provides:       libfprint-devel = %{epoch}:%{version}-%{release}
Obsoletes:      libfprint-devel < %{epoch}:%{version}-%{release}

%description
libfprint with the elanpress driver for the ELAN 04f3:0c6e press sensor
used in several ASUS laptops. This build tracks commit fa2f98f of the
elanpress branch and replaces the distribution libfprint package.

The fork speaks the press protocol. The distribution driver treats this
sensor as a swipe device and fails identification with a protocol error.

Epoch 1 keeps dnf from replacing this package with the newer upstream
version shipped by Fedora. Remove this repository and reinstall libfprint
from Fedora to return to the distribution build.

%prep
%autosetup -n libfprint-%{version}

%build
%meson \
  -Ddoc=false \
  -Dinstalled-tests=false \
  -Dgtk-examples=false \
  -Dudev_rules=enabled \
  -Dudev_hwdb=enabled
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md AUTHORS NEWS THANKS
%{_libdir}/libfprint-2.so
%{_libdir}/libfprint-2.so.2
%{_libdir}/libfprint-2.so.2.*
%{_libdir}/pkgconfig/libfprint-2.pc
%{_libdir}/girepository-1.0/FPrint-2.0.typelib
%{_includedir}/libfprint-2/
%{_datadir}/gir-1.0/FPrint-2.0.gir
%{_udevrulesdir}/70-libfprint-2.rules
%{_udevhwdbdir}/60-autosuspend-libfprint-2.hwdb
%{_datadir}/metainfo/org.freedesktop.libfprint.metainfo.xml

%changelog
* Fri Oct 30 2026 Yovcho Yovchev <iovcho.iovchev@gmail.com> - 1:1.94.10-1.elanpress.fa2f98f
- Package the elanpress fork for Fedora, pinned to fa2f98f.
