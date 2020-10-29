Summary:        A utility for generating programs that recognize patterns in text
Name:           flex
Version:        2.6.4
Release:        6%{?dist}
License:        BSD
URL:            https://github.com/westes/flex
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/westes/flex/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  m4
Requires:       m4
# Upstream community decided to not fix this
Patch0:         CVE-2019-6293.nopatch

%description
The Flex package contains a utility for generating programs
that recognize patterns in text.

%package devel
Summary: Development libraries and header files for the flex library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The flex-devel package contains the development libraries and header files for
flex.

%prep
%setup -q
sed -i -e '/test-bison/d' tests/Makefile.in
%build
CFLAGS="-D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
cat > %{buildroot}/usr/bin/lex <<- "EOF"
#!/bin/sh
# Begin /usr/bin/lex

	exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/flex
%{_bindir}/flex++
%attr(755,root,root) %{_bindir}/lex
%{_libdir}/*.so.*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
*   Thu Oct 29 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.6.4-6
-   No patch CVE-2019-6293

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.6.4-5
-   Added %%license line automatically

*   Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> 2.6.4-4
-   Fix URL.
-   License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.6.4-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Aug 4 2017 Alexey Makhalov <amakhalov@vmware.com> 2.6.4-2
-   Use _GNU_SOURCE

*   Thu May 11 2017 Chang Lee <changlee@vmware.com> 2.6.4-1
-   Updated to version 2.6.4

*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 2.6.0-1
-   Updated to version 2.6.0

*   Thu Oct 13 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.39-3
-   Fixing Security bug CVE-2016-6354.

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.39-2
-   GA - Bump release of all rpms

*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5.39-1
-   Updated to version 2.5.39

*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.5.38-3
-   Moving static lib files to devel package.

*   Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.5.38-2
-   Adding m4 package to build and run time required package

*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.5.38-1
-   Initial build. First version
