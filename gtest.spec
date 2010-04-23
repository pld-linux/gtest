# TODO
# - libgtest.so needs -lpthread
# - tests fail due some linkage problems
#
# Conditional build:
%bcond_with	tests		# build without tests.

Summary:	Google C++ testing framework
Name:		gtest
Version:	1.5.0
Release:	1
License:	BSD
Group:		Development/Tools
URL:		http://code.google.com/p/googletest/
Source0:	http://googletest.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	8b2c3c3f26cb53e64a3109d03a97200a
BuildRequires:	libtool
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
cp -a samples examples

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%{__libtoolize}
%configure \
	--disable-static

%{__make}

%{?with_tests:make check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
%attr(755,root,root) %{_bindir}/%{name}-config
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/internal
%{_aclocaldir}/%{name}.m4
%{_examplesdir}/%{name}-%{version}
