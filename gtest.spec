#
# Conditional build:
%bcond_without	tests		# do not perform "make check"
#
Summary:	Google C++ testing framework
Summary(pl.UTF-8):	Szkielet testów w C++ stworzony przez Google
Name:		gtest
Version:	1.7.0
Release:	5
License:	BSD
Group:		Development/Tools
#Source0Download: https://github.com/google/googletest/releases
#Source0:	https://github.com/google/googletest/archive/release-%{version}/%{name}-%{version}.tar.gz
Source0:	http://googletest.googlecode.com/files/%{name}-%{version}.zip
# Source0-md5:	2d6ec8ccdf5c46b05ba54a9fd1d130d7
Patch0:		%{name}-install.patch
Patch1:		%{name}-link.patch
URL:		https://github.com/google/googletest
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python >= 2.3
BuildRequires:	python-modules >= 2.3
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Google's framework for writing C++ tests on a variety of platforms
(GNU/Linux, Mac OS X, Windows, Windows CE, and Symbian). Based on the
xUnit architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.

%description -l pl.UTF-8
Stworzony przez Google szkielet do pisania testów w C++ na różnych
platformach (GNU/Linux, Mac OS X, Windows, Windows CE, Symbian). Jest
oparty na architekturze xUnit. Obsługuje automatyczne wykrywanie
testów, bogaty zbiór zapewnień, zapewnienia zdefiniowane przez
użytkownika, testy śmierci, niepowodzenia krytyczne i niekrytyczne,
różne opcje uruchamiania testów oraz tworzenie raportów z testów w
XML-u.

%package devel
Summary:	Development files for gtest framework
Summary(pl.UTF-8):	Pliki programistyczne szkieletu gtest
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This package contains development files for gtest framework.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne szkieletu gtest.

%package static
Summary:	Static gtest libraries
Summary(pl.UTF-8):	Statyczne biblioteki gtest
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gtest libraries.

%description static -l pl.UTF-8
Statyczne biblioteki gtest.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Keep a clean copy of samples.
cp -a samples examples

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp scripts/gtest-config $RPM_BUILD_ROOT%{_bindir}/gtest-config

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_prefix}/src/gtest/src
cp -p src/*.{cc,h} $RPM_BUILD_ROOT%{_prefix}/src/gtest/src
cp -pr CMakeLists.txt cmake $RPM_BUILD_ROOT%{_prefix}/src/gtest

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES CONTRIBUTORS LICENSE README
%attr(755,root,root) %{_libdir}/libgtest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtest.so.0
%attr(755,root,root) %{_libdir}/libgtest_main.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgtest_main.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtest-config
%attr(755,root,root) %{_libdir}/libgtest.so
%attr(755,root,root) %{_libdir}/libgtest_main.so
%{_libdir}/libgtest.la
%{_libdir}/libgtest_main.la
%{_includedir}/gtest
%{_aclocaldir}/gtest.m4
%{_prefix}/src/gtest
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libgtest.a
%{_libdir}/libgtest_main.a
