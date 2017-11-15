Name:           cygwin-pkg-config
Version:        0.29.1
Release:        1%{?dist}
Summary:        A tool for determining compilation options

License:        GPLv2+
Group:          Development/Tools
URL:            http://pkgconfig.freedesktop.org
Source0:        http://www.freedesktop.org/software/pkgconfig/releases/pkg-config-%{version}.tar.gz

BuildRequires:  glib2-devel
BuildRequires:  cygwin32-filesystem >= 7
BuildRequires:  cygwin64-filesystem >= 7


%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.


# Cygwin32
%package -n cygwin32-pkg-config
Summary:        A tool for determining compilation options for the Cygwin32 target
Requires:       cygwin32-filesystem >= 7

%description -n cygwin32-pkg-config
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

# Cygwin64
%package -n cygwin64-pkg-config
Summary:        A tool for determining compilation options for the Cygwin64 target
Requires:       cygwin64-filesystem >= 7

%description -n cygwin64-pkg-config
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.


%prep
%setup -q -n pkg-config-%{version}


%build
%global _configure ../configure

mkdir build_cyg32
pushd build_cyg32
    %configure \
        --disable-shared \
        --disable-host-tool \
        --program-prefix=%{cygwin32_target}- \
        --with-pc-path=%{cygwin32_libdir}/pkgconfig:%{cygwin32_datadir}/pkgconfig:%{_datadir}/pkgconfig \
	--with-system-include-path=%{cygwin32_includedir} \
	--with-system-library-path=%{cygwin32_libdir}

    make %{?_smp_mflags}
popd

mkdir build_cyg64
pushd build_cyg64
    %configure \
        --disable-shared \
        --disable-host-tool \
        --program-prefix=%{cygwin64_target}- \
        --with-pc-path=%{cygwin64_libdir}/pkgconfig:%{cygwin64_datadir}/pkgconfig:%{_datadir}/pkgconfig \
	--with-system-include-path=%{cygwin64_includedir} \
	--with-system-library-path=%{cygwin64_libdir}

    make %{?_smp_mflags}
popd


%install
make install -C build_cyg32 DESTDIR=$RPM_BUILD_ROOT m4dir=%{cygwin32_datadir}/aclocal
make install -C build_cyg64 DESTDIR=$RPM_BUILD_ROOT m4dir=%{cygwin64_datadir}/aclocal

# These files conflict with ordinary pkg-config.
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/pkg-config


%files -n cygwin32-pkg-config
%doc AUTHORS README NEWS COPYING pkg-config-guide.html
%{_bindir}/%{cygwin32_target}-pkg-config
%{_mandir}/man1/%{cygwin32_target}-pkg-config.1*
%{cygwin32_datadir}/aclocal/pkg.m4

%files -n cygwin64-pkg-config
%doc AUTHORS README NEWS COPYING pkg-config-guide.html
%{_bindir}/%{cygwin64_target}-pkg-config
%{_mandir}/man1/%{cygwin64_target}-pkg-config.1*
%{cygwin64_datadir}/aclocal/pkg.m4


%changelog
* Mon Sep 12 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.29.1-1
- new version

* Mon Jan 20 2014 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.28-3
- Install aclocal macros in the sysroots.

* Thu Jun 27 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.28-2
- Configure system include and library paths to avoid -I and -L flags.

* Wed Jun 26 2013 Yaakov Selkowitz <cygwin-ports-general@lists.sourceforge.net> - 0.28-1
- Initial spec file, largely based on mingw-pkg-config.
