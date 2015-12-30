Name:           mpv
Version:        0.14.0
Release:        1%{?dist}
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+
URL:            http://%{name}.io/
Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz

# set defaults for Fedora
Patch0:         %{name}-config.patch

# Upstream commit to use waf >= 1.8 (reverted, rebased)
# See https://github.com/mpv-player/mpv/issues/1363
Patch1:         %{name}-old-waf.patch

BuildRequires:  aalib-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bzip2-devel
BuildRequires:  compat-lua-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  ffmpeg-libs
BuildRequires:  lcms2-devel
BuildRequires:  libcdio-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  libGL-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXv-devel
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libguess-devel
BuildRequires:  libquvi-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  lirc-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  ncurses-devel
BuildRequires:  perl-Encode
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-docutils
BuildRequires:  waf
BuildRequires:  wayland-devel

%if 0%{?fedora} >= 23
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-bignum
%endif

Requires:       hicolor-icon-theme

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package -n libmpv
Summary: Dynamic library for Mpv frontends 

%description -n libmpv
This package contains the dynamic library libmpv, which provides access to Mpv.

%package -n libmpv-devel
Summary: Development package for libmpv
Requires: libmpv%{_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libmpv-devel
Libmpv development header files and libraries.

%prep
%setup -q
%patch0 -p1

%if 0%{?fedora} < 22
%patch1 -p1
%endif


%build
CCFLAGS="%{optflags}" \
waf configure \
    --prefix="%{_prefix}" \
    --bindir="%{_bindir}" \
    --libdir="%{_libdir}" \
    --mandir="%{_mandir}" \
    --docdir="%{_docdir}/%{name}" \
    --confdir="%{_sysconfdir}/%{name}" \
    --disable-sdl1 --disable-sdl2 \
    --disable-build-date \
    --enable-libmpv-shared

waf build --verbose %{?_smp_mflags}

%install
waf --destdir=%{buildroot} install %{?_smp_mflags}

# Default config files
install -Dpm 644 etc/example.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -Dpm 644 etc/input.conf %{buildroot}%{_sysconfdir}/%{name}/input.conf

desktop-file-install etc/mpv.desktop

for RES in 16 32 64; do
  install -Dpm 644 etc/mpv-icon-8bit-${RES}x${RES}.png %{buildroot}%{_datadir}/icons/hicolor/${RES}x${RES}/apps/%{name}.png
done
install -Dpm 644 etc/%{name}-gradient.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-gradient.svg
install -Dpm 644 etc/%{name}-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg
install -Dpm 644 etc/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%post
update-desktop-database &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%post -n libmpv -p /sbin/ldconfig

%postun -n libmpv -p /sbin/ldconfig

%files
%doc LICENSE README.md Copyright
%doc %{_docdir}/%{name}/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf
%config(noreplace) %{_sysconfdir}/%{name}/input.conf

%files -n libmpv
%doc LICENSE README.md Copyright
%{_libdir}/libmpv.so.*

%files -n libmpv-devel
%{_includedir}/%{name}
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Sat Dec 12 2015 Evgeny Lensky <surfernsk@gmail.com> - 0.14.0-2
- add svg icons

* Sat Dec 12 2015 Evgeny Lensky <surfernsk@gmail.com> - 0.14.0-1
- update to 0.14.0

* Thu Nov 26 2015 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-2
- Add mesa-libEGL-devel to BRs

* Thu Nov 26 2015 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-1
- Updated to 0.13.0

* Thu Jun 11 2015 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-2
- Removed --disable-debug flag

* Wed Jun 10 2015 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-1
- Updated to 0.9.2
- Also build the library

* Sat May 16 2015 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-1
- Update to 0.9.1
- BR compat-lua-devel because mpv does not work with lua 5.3
- Add BR lcms2-devel (#3643)
- Removed --enable-joystick and --enable-lirc (no longer used)

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-3
- Conditionalize old waf patch

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-2
- Rebuilt

* Mon Apr 13 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-1
- Updated

* Wed Jan 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-1
- Updated

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Slightly change the waf patch

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-2
- Add patch to allow waf 1.7

* Sat Dec 13 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-1
- New version 0.7.1
- Rebuilt new lirc (#3450)

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-3
- Rebuilt for vaapi 0.36

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.6.0-2
- Rebuilt for FFmpeg 2.4.3

* Sun Oct 12 2014 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-1
- New version 0.6.0

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-2
- Rebuilt for FFmpeg 2.4.x

* Wed Sep 03 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-1
- New version 0.5.1
- Add BR ncurses-devel (#3233)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.4.0-2
- Rebuilt for ffmpeg-2.3

* Tue Jul 08 2014 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- New version 0.4.0

* Tue Jun 24 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.11-1
- New version 0.3.11

* Tue Mar 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-2
- Rebuilt for new libcdio and libass

* Thu Mar 20 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-1
- New version 0.3.6

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-2
- Rebuilt for mistake

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-1
- New version 0.3.5

* Sat Jan 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-1
- New version 0.3.3

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Use upstream .desktop file

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-1
- New version 0.3.0
- Switch to waf
- Add some tricks from openSUSE
- Removed already included patch

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-8
- Added patch for https://fedoraproject.org/wiki/Changes/FormatSecurity

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-7
- Support wayland

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-6
- Rebuilt

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-5
- Fixed wrong license tag (see upstream a5507312)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-4
- Added libva (#3065)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-3
- Added lua and libquvi (#3025)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-2
- Rebuilt for mistakes

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-1
- New version 0.2.4

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-4
- There's no longer AUTHORS file in %%doc
- Install icons

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-3
- Rebased config patch

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-2
- Proper sources for all branches

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-1
- New upstream version

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-4
- Fixing cvs errors

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-3
- Add desktop file

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-2
- Do not use xv as default vo

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-1
- New upstream release

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-4
- Rebuilt

* Mon Sep 09 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-3
- Added BR ffmpeg-libs

* Tue Aug 27 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-2
- Reduced BRs a lot (removed support for various stuff)
- Make smbclient realized
- Changed the description to the text from manual page

* Mon Aug 19 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-1
- Initial spec
- Inspired a lot in mplayer.spec

