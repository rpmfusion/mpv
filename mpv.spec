Name:           mpv
Version:        0.2.3
Release:        2%{?dist}
Summary:        Movie player playing most video formats and DVDs
License:        GPLv3+
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
BuildRequires:  libass-devel
BuildRequires:  libbluray-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libGL-devel
BuildRequires:  libsmbclient-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXv-devel
BuildRequires:  lirc-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  python-docutils

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
desktop-file-install %{SOURCE1}

%files
%doc AUTHORS LICENSE README.md Copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%changelog
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

