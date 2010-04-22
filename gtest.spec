#
# Conditional build:
%bcond_without	tests		# build without tests.

Summary:	Google C++ testing framework
Name:		gtest
Version:	1.4.0
Release:	1
License:	BSD
Group:		Development/Tools
URL:		http://code.google.com/p/googletest/
Source0:	http://googletest.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	c91de493522cf1b75902d3b3730ff8de
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google's framework for writing C++ tests on a variety of platforms
(GNU/Linux, Mac OS X, Windows, Windows CE, and Symbian). Based on the
xUnit architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

# Keep a clean copy of samples.
cp -pr samples samples.orig

%build
%configure \
	--disable-static

# Omit unused direct shared library dependencies.
# XXX: in pld libtool is patched?
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%{__make}

# Two tests fail here, unclear as to why.
%{?with_tests:make check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -delete

# Restore the clean copy of samples.
# To be later listed against %doc.
rm -rf samples
cp -a samples.orig samples

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS README
%attr(755,root,root) %{_libdir}/libgtest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtest.so.0
%attr(755,root,root) %{_libdir}/libgtest_main.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtest_main.so.0

%files devel
%defattr(644,root,root,755)
%doc samples
%attr(755,root,root) %{_bindir}/%{name}-config
%{_aclocaldir}/%{name}.m4
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so

%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/internal
