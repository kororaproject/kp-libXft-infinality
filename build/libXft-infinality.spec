Summary: X.Org X11 libXft runtime library
Name: libXft-infinality
Version: 2.2.0
Release: 2%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1: libXft-2.2.0-ubuntu.patch

Source0: ftp://ftp.x.org/pub/individual/lib/libXft-%{version}.tar.bz2

BuildRequires: xorg-x11-proto-devel
BuildRequires: libX11-devel
BuildRequires: libXrender-devel
BuildRequires: freetype-devel >= 2.1.9-2
BuildRequires: fontconfig-devel >= 2.2-1

Requires: fontconfig >= 2.2-1

%description
X.Org X11 libXft runtime library

This version is patched with the Ubuntu patch.

#%package devel
#Summary: X.Org X11 libXft development package
#Group: Development/Libraries
#Requires(pre): xorg-x11-filesystem >= 0.99.2-3
#Requires: %{name} = %{version}-%{release}

#Requires: xorg-x11-proto-devel pkgconfig
#Requires: libXrender-devel
#Requires: fontconfig-devel >= 2.2-1
#Requires: freetype-devel >= 2.1.9-2

  

#%description devel
#X.Org X11 libXft development package

%prep
%setup -q -n libXft-%{version}

%patch1 -p1 -b .lcdfilter

# Disable static library creation by default.
%define with_static 0

%build

%configure \
%if ! %{with_static}
	--disable-static
%endif
make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Don't package static a or .la files nor devel files
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.{a,la,so} \
       $RPM_BUILD_ROOT%{_libdir}/pkgconfig $RPM_BUILD_ROOT%{_bindir} \
       $RPM_BUILD_ROOT%{_datadir}/aclocal $RPM_BUILD_ROOT%{_includedir}

# Move library to avoid conflict with official FreeType package
mkdir $RPM_BUILD_ROOT%{_libdir}/%{name}
mv -f $RPM_BUILD_ROOT%{_libdir}/libXft.so.* \
      $RPM_BUILD_ROOT%{_libdir}/%{name}

# Register the library directory in /etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
     >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

/bin/echo "PRELOAD=1; if [ -f /etc/sysconfig/fonts ]; then . /etc/sysconfig/fonts; fi; A1=\`arch\`; A2=%{_arch}; if [ \"\${A1:0:1}\" = \"\${A2:0:1}\" -a ! \"\$PRELOAD\" = \"0\" ]; then ADDED=\`/bin/echo \$LD_PRELOAD | grep \"%{_libdir}/libXft.so.2\" | wc -l\`; if [ \"\$ADDED\" = \"0\" ]; then export LD_PRELOAD=%{_libdir}/%{name}/libXft.so.2:\$LD_PRELOAD ; fi; fi" > $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/%{name}-%{_arch}.sh


# FIXME: There's no real good reason to ship these anymore, as pkg-config
# is the official way to detect flags, etc. now.
rm -f $RPM_BUILD_ROOT%{_bindir}/xft-config
rm -rf $RPM_BUILD_ROOT%{_mandir}/

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_libdir}/%{name}/libXft.so.2*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%{_sysconfdir}/profile.d/%{name}-%{_arch}.sh

#%files devel
#%defattr(-,root,root,-)
#%{_bindir}/xft-config
#%dir %{_includedir}/X11
#%dir %{_includedir}/X11/Xft
#%{_includedir}/X11/Xft/Xft.h
#%{_includedir}/X11/Xft/XftCompat.h
#%if %{with_static}
#%{_libdir}/libXft.a
#%endif
#%{_libdir}/libXft.so
#%{_libdir}/pkgconfig/xft.pc
#%{_mandir}/man1/xft-config.1.gz
#%dir %{_mandir}/man3x
#%{_mandir}/man3/Xft.3*

%changelog
* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 2.2.0-1
- libXft 2.2.0

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 2.1.14-1
- libXft 2.1.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.1.13-3
- Un-require xorg-x11-filesystem
- Remove useless %%dir

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Adam Jackson <ajax@redhat.com> 2.1.13-1
- libXft 2.1.13

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.12-5
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 parag <paragn@fedoraproject.org> - 2.1.12-4
- Merge-Review #226074
- Removed XFree86-libs, xorg-x11-libs XFree86-devel, xorg-x11-devel as Obsoletes
- Removed BR:pkgconfig
- Removed zero-length NEWS file

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 2.1.12-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 2.1.12-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 2.1.12-1.fc7
- Update to 2.1.12

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 2.1.10
- Updated libXft to version 2.1.10
- Specify freetype dependencies as >= 2.1.9-1
- Futureproof builds by adding release number to fontconfig dependencies.

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-4
- Replace "makeinstall" with "make install DESTDIR=..."

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 2.1.8.2-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 2.1.8.2-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-3
- Added missing dependencies to devel subpackage to fix (#176744)

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 2.1.8.2-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 2.1.8.2-1
- Updated libXft to version 2.1.8.2 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 2.1.8.1-1
- Updated libXft to version 2.1.8.1 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.
- Added "Requires: libXrender-devel" to -devel subpackage for (#175465)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 2.1.8-2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'

* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 2.1.8-1
- Updated libXft to version 2.1.8 from X11R7 RC1

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-5
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro
- Fix BuildRequires to use new style X library package names

* Sun Sep 04 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-4
- Added "BuildRequires: fontconfig-devel >= 2.2" dependency that was
  previously missed.  Also added "Requires: fontconfig >= 2.2" runtime
  dependency.
- Added missing defattr to devel subpackage.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-3
- Added freetype-devel build dependency.

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 2.1.7-1
- Initial build.
