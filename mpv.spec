%global commit c9e7473d67893d9248bedf63530a1e0325a3036a
%global gitdate 20190616
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrelease .%{gitdate}.git%{shortcommit}

Name:           mpv
Version:        0.29.1
Release:        8%{?gitrelease}%{?dist}
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+ and LGPLv2+
URL:            http://mpv.io/
Source0:        https://github.com/mpv-player/mpv/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# set defaults for Fedora
Patch0:         %{name}-config.patch

# Fix ppc as upstream refuse to fix the issue
# https://github.com/mpv-player/mpv/issues/3776
Patch1:         ppc_fix.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enca)
BuildRequires:  pkgconfig(libavutil) >= 56.12.100
BuildRequires:  pkgconfig(libavcodec) >= 58.16.100
BuildRequires:  pkgconfig(libavformat) >= 58.9.100
BuildRequires:  pkgconfig(libswscale) >= 5.0.101
BuildRequires:  pkgconfig(libavfilter) >= 7.14.100
BuildRequires:  pkgconfig(libswresample) >= 3.0.100
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(mujs)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libplacebo)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libquvi-0.9)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(lua-5.1)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  libshaderc-devel
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet) >= 0.0.5
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  waf
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  /usr/bin/rst2man
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  perl(Encode)

%ifarch armv7hl armv7hnl
%{?_with_rpi:
BuildRequires:  raspberrypi-vc-devel
}
%endif

# Obsoletes older ci/cd
Obsoletes:  mpv-master < %{version}-100
Provides: mpv-master = %{version}-100

Requires:       hicolor-icon-theme
Provides:       mplayer-backend

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%package libs
Summary: Dynamic library for Mpv frontends 

%description libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package libs-devel
Summary: Development package for libmpv
Requires: mpv-libs%{?_isa} = %{version}-%{release}

%description libs-devel
Libmpv development header files and libraries.

%prep
%autosetup -p1 -n mpv-%{?commit}%{?!commit:%{version}}

sed -i -e "s|c_preproc.standard_includes.append('/usr/local/include')|c_preproc.standard_includes.append('$(pkgconf --variable=includedir libavcodec)')|" wscript


%build
%set_build_flags
%{_bindir}/waf configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_docdir}/%{name} \
    --confdir=%{_sysconfdir}/%{name} \
    --disable-build-date \
    --enable-libmpv-shared \
    --enable-sdl2 \
    --enable-libarchive \
    --enable-libsmbclient \
    --enable-dvdread \
    --enable-dvdnav \
    --enable-cdda \
%{?_with_rpi:--enable-rpi --disable-vaapi} \
    --enable-tv \
    --enable-dvbin
    

%{_bindir}/waf -v build %{?_smp_mflags}

%install
%{_bindir}/waf install --destdir=%{buildroot}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 644 README.md etc/input.conf etc/mpv.conf -t %{buildroot}%{_docdir}/%{name}/

%files
%docdir %{_docdir}/%{name}/
%{_docdir}/%{name}/
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%{_mandir}/man1/%{name}.*
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_libdir}/libmpv.so.*

%files libs-devel
%{_includedir}/%{name}/
%{_libdir}/libmpv.so
%{_libdir}/pkgconfig/mpv.pc

%changelog
* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 0.29.1-8.20190616.gitc9e7473
- Update to 20190616 snapshot
- Add libplacebo
- Fix support for FFmpeg DRM PRIME

* Sun Jun 23 2019 Leigh Scott <leigh123linux@googlemail.com> - 0.29.1-6
- Rebuild against sdk9 nv-codec-headers
- Spec file clean up

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.29.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 0.29.1-4
- Enable JavaScript support (rfbz#5151)

* Tue Dec 18 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.29.1-3
- Enable rpi support

* Tue Nov 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.29.1-2
- Rebuild for new ffmpeg

* Sat Oct 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.29.1-1
- Update to 0.29.1
- Drop old Obsoletes and Provides
- Use modern marcos

* Tue Oct 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.29.0-3
- Add BuildRequires: libshaderc-devel

* Thu Aug 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.29.0-2
- Add BuildRequires: gcc

* Wed Jul 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.29.0-1
- Update to 0.29.0

* Wed Jun 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.2-6
- Revert last commit

* Sat Jun 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.2-5
- Rebuild for new libass version
- vulkan is x86 only

* Fri Apr 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.2-4
- Rebuild for ffmpeg-4.0 release

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.28.2-3
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.2-1
- Update to 0.28.2

* Sun Feb 11 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.1-1
- Update to 0.28.1

* Thu Feb 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.0-3
- Fix missing build requires

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.0-2
- Rebuild for libcdio

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.28.0-1
- Update to 0.28.0
- Enable VA-API
- Enable vulkan support

* Tue Jan 16 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.27.0-4
- Disable VA-API until 0.28.0 lands

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.27.0-3
- Rebuilt for VA-API 1.0.0

* Mon Oct 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.27.0-2
- Rebuild for ffmpeg update

* Fri Sep 15 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.27.0-1
- Update to 0.27.0
- Enable libarchive support (play .zip, .iso and other formats)

* Fri Aug 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.26.0-3
- Enable Samba support  (rfbz#4624)
- Enable TV and DVB support

* Wed Aug 09 2017 Miro Hrončok <mhroncok@redhat.com> - 0.26.0-2
- Enable DVD and CDDA support  (rfbz#4622)

* Thu Jul 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.26.0-1
- Update to 0.26.0

* Wed May 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.25.0-2
- Rebuild for ffmpeg update

* Mon May 08 2017 Miro Hrončok <mhroncok@redhat.com> - 0.25.0-1
- Update to 0.25.0

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.24.0-2
- Rebuild for ffmpeg update

* Sun Apr 02 2017 Miro Hrončok <mhroncok@redhat.com> - 0.24.0-1
- Update to 0.24.0

* Thu Mar 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.23.0-4
- Try to fix ppc build

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.23.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-2
- Fix AVAudioResampleContext: Unable to set resampling compensation (rfbz#4408)

* Sat Dec 31 2016 Miro Hrončok <mhroncok@redhat.com> - 0.23.0-1
- Update to 0.23.0

* Sat Dec 03 2016 leigh scott <leigh123linux@googlemail.com> - 0.22.0-2
- Add patch to relax ffmpeg version check

* Sat Nov 26 2016 leigh scott <leigh123linux@googlemail.com> - 0.22.0-1
- update to 0.22.0

* Thu Nov 17 2016 Adrian Reber <adrian@lisas.de> - 0.21.0-3
- Rebuilt for libcdio-0.94

* Sat Nov 05 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.21.0-2
- Rebuilt for new ffmpeg
- Add provides mplayer-backend (rfbz#4284)

* Thu Oct 20 2016 Evgeny Lensky <surfernsk@gmail.com> - 0.21.0-1
- update to 0.21.0

* Tue Aug 16 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.19.0-3
- Update to 0.19.0
- Add LDFLAGS so build is hardened
- Fix CFLAGS
- Make build verbose
- Remove Requires pkgconfig from devel sub-package
- Fix source tag

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.18.1-2
- Rebuilt for ffmpeg-3.1.1

* Tue Jul 26 2016 Miro Hrončok <mhroncok@redhat.com> - 0.18.1-1
- Update to 0.18.1
- Remove patch for Fedora < 22

* Sun Jul 03 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-3
- BRs in alphabetical order, rename of sub-packages libs and other improvements

* Thu Jun 30 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-2
- Add BR perl(Encode) to build on F24 (merge from Adrian Reber PR)

* Tue Jun 28 2016 Sérgio Basto <sergio@serjux.com> - 0.18.0-1
- Update to 0.18.0

* Mon Apr 11 2016 Evgeny Lensky <surfernsk@gmail.com> - 0.17.0-1
- update to 0.17.0

* Mon Feb 29 2016 Evgeny Lensky <surfernsk@gmail.com> - 0.16.0-1
- update to 0.16.0
- edit mpv-config.patch

* Sun Feb 14 2016 Sérgio Basto <sergio@serjux.com> - 0.15.0-2
- Drop BR lirc, because support for LIRC has been removed in mpv 0.9.0.
- Add license tag.
- libmpv-devel does not need have same doc and license files.

* Thu Jan 21 2016 Evgeny Lensky <surfernsk@gmail.com> - 0.15.0-1
- update to 0.15.0

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
