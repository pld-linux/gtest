#
# Conditional build:
%bcond_without	tests		# do not perform "make check"
#
Summary:	Google C++ testing framework
Summary(pl.UTF-8):	Szkielet testów w C++ stworzony przez Google
Name:		gtest
Version:	1.8.1
Release:	1
License:	BSD
Group:		Development/Tools
#Source0Download: https://github.com/google/googletest/releases
Source0:	https://github.com/google/googletest/archive/release-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2e6fbeb6a91310a16efe181886c59596
Patch0:		%{name}-install.patch
Patch1:		%{name}-link.patch
Patch2:		gmock-install.patch
URL:		https://github.com/google/googletest
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	python >= 2.3
BuildRequires:	python-modules >= 2.3
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

%package -n gmock-devel
Summary:	Google C++ Mocking Framework
Summary(pl.UTF-8):	Szkielet Google Mock dla C++
Group:		Development/Libraries
Requires:	gtest-devel = %{version}-%{release}
Requires:	libstdc++-devel
Provides:	gmock = %{version}-%{release}
Obsoletes:	gmock < 1.6.0-3

%description -n gmock-devel
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++'s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:
- lets you create mock classes trivially using simple macros,
- supports a rich set of matchers and actions,
- handles unordered, partially ordered, or completely ordered
  expectations,
- is extensible by users, and
- works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
  Symbian.

%description -n gmock-devel -l pl.UTF-8
Google C++ Mocking Framework (w skrócie Google Mock) to zainspirowana
przez jMock, EasyMock i Hamcrest, zaprojektowana z myślą o specyfice
C++ biblioteka do pisania i wykorzystywania klas "mock" w C++.

Google Mock:
- pozwala tworzyć klasy "mock" w sposób trywialny przy użyciu makr;
- obsługuje bogaty zbiór dopasowań i akcji;
- obsługuje oczekiwania nieuporządkowane, częściowo uporządkowane
  lub w pełni uporządkowane;
- jest rozszerzalna dla użytkownika;
- działa na Linuksie, Mac OS X, Windows, Windows Mobile, minGW oraz
  Symbianie.


%prep
%setup -q -n googletest-release-%{version}

cd googletest
%patch0 -p1
%patch1 -p1
# Keep a clean copy of samples.
cp -a samples examples

cd ../googlemock
%patch2 -p1
grep -rl bin/env scripts | xargs %{__sed} -i -e '1s,^#!.*python,#!%{__python},'


%build
cd googletest
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%{?with_tests:%{__make} check}

cd ../googlemock
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	GTEST_CONFIG=../googletest/scripts/gtest-config \
	GTEST_CPPFLAGS="-I$PWD/../googletest/include" \
	GTEST_LDFLAGS="-L$PWD/../googletest/lib/.libs" \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

cd googletest
%{__make} -j1 install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp scripts/gtest-config $RPM_BUILD_ROOT%{_bindir}/gtest-config

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_prefix}/src/gtest/src
cp -p src/*.{cc,h} $RPM_BUILD_ROOT%{_prefix}/src/gtest/src
cp -pr CMakeLists.txt cmake $RPM_BUILD_ROOT%{_prefix}/src/gtest

cd ../googlemock
%{__make} -j1 install \
	INSTALL="%{__install} -p" \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/gmock/generator/{README.cppclean,LICENSE,README}
# gmock CMakeLists.txt expects gtest or ../googletest accessile
ln -snf ../gtest $RPM_BUILD_ROOT%{_prefix}/src/gmock/gtest

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc googletest/{CHANGES,CONTRIBUTORS,LICENSE,README.md}
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

%files -n gmock-devel
%defattr(644,root,root,755)
%doc googlemock/{CHANGES,CONTRIBUTORS,LICENSE,README.md}
%attr(755,root,root) %{_bindir}/gmock-config
%{_includedir}/gmock
%{_npkgconfigdir}/gmock.pc
%dir %{_datadir}/gmock
%dir %{_datadir}/gmock/generator
%attr(755,root,root) %{_datadir}/gmock/generator/gmock_gen.py
%dir %{_datadir}/gmock/generator/cpp
%attr(755,root,root) %{_datadir}/gmock/generator/cpp/*.py
%{_prefix}/src/gmock
