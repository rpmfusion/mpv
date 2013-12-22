Name:           mpv
Version:        0.2.4
Release:        6%{?dist}
Summary:        Movie player playing most video formats and DVDs
License:        GPLv2+
URL:            http://%{name}.io/
Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz
Source1:        %{name}.desktop

# set defaults for Fedora
Patch0:         %{name}-config.patch

BuildRequires:  aalib-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bzip2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  ffmpeg-libs
BuildRequires:  libGL-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXv-devel
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libquvi-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
BuildRequires:  lirc-devel
BuildRequires:  lua-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-docutils

Requires:       hicolor-icon-theme

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

%prep
%setup -q
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --mandir=%{_mandir} \
    --confdir=%{_sysconfdir}/%{name} \
    --extra-cflags="$RPM_OPT_FLAGS" \
    --enable-joystick \
    --enable-lirc \
    --enable-radio \
    --enable-radio-capture \
    --enable-smb \
    --disable-termcap \
    --extra-cflags='-I/usr/include/samba-4.0/'

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Default config files
install -Dpm 644 etc/example.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -Dpm 644 etc/input.conf %{buildroot}%{_sysconfdir}/%{name}/input.conf

desktop-file-install %{SOURCE1}

for RES in 16 32 64; do
  install -Dpm 644 etc/mpv-icon-8bit-${RES}x${RES}.png %{buildroot}%{_datadir}/icons/hicolor/${RES}x${RES}/apps/%{name}.png
done

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

%files
%doc LICENSE README.md Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/input.conf

%changelog
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

