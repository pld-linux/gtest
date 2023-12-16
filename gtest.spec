#
# Conditional build:
%bcond_with	tests		# unit tests (supported only using bazel)
%bcond_without	static_libs	# static libraries
#
Summary:	Google C++ testing framework
Summary(pl.UTF-8):	Szkielet testów w C++ stworzony przez Google
Name:		gtest
Version:	1.14.0
Release:	1
License:	BSD
Group:		Development/Tools
#Source0Download: https://github.com/google/googletest/releases
Source0:	https://github.com/google/googletest/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c8340a482851ef6a3fe618a082304cfc
Patch0:		cmake.patch
URL:		https://github.com/google/googletest
BuildRequires:	cmake >= 3.13
BuildRequires:	libstdc++-devel >= 6:5
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
Requires:	libstdc++-devel >= 6:5

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

%package src
Summary:	Source code of gtest framework
Summary(pl.UTF-8):	Kod źródłowy szkieletu gtest
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description src
Source code of gtest framework for embedding it in other projects.

%description src -l pl.UTF-8
Kod źródłowy szkieletu gtest do osadzania go w innych projektach.

%package -n gmock
Summary:	Google C++ Mocking Framework
Summary(pl.UTF-8):	Szkielet Google Mock dla C++
Group:		Libraries
Requires:	gtest = %{version}-%{release}

%description -n gmock
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

%description -n gmock -l pl.UTF-8
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

%package -n gmock-devel
Summary:	Development files for gmock framework
Summary(pl.UTF-8):	Pliki programistyczne szkieletu gmock
Group:		Development/Libraries
Requires:	gmock = %{version}-%{release}
Requires:	gtest-devel = %{version}-%{release}

%description -n gmock-devel
This package contains development files for gmock framework.

%description -n gmock-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne szkieletu gmock.

%package -n gmock-static
Summary:	Static gmock libraries
Summary(pl.UTF-8):	Statyczne biblioteki gmock
Group:		Development/Libraries
Requires:	gmock-devel = %{version}-%{release}

%description -n gmock-static
Static gmock libraries.

%description -n gmock-static -l pl.UTF-8
Statyczne biblioteki gmock.

%package -n gmock-src
Summary:	Source code of gmock framework
Summary(pl.UTF-8):	Kod źródłowy szkieletu gmock
Group:		Development/Libraries
Requires:	%{name}-src = %{version}-%{release}
Requires:	gmock-devel = %{version}-%{release}

%description -n gmock-src
Source code of gmock framework for embedding it in other projects.

%description -n gmock-src -l pl.UTF-8
Kod źródłowy szkieletu gmock do osadzania go w innych projektach.

%prep
%setup -q -n googletest-%{version}
%patch0 -p1

%build
# Note: official build system is now Bazel - but it's extremely distro unfriendly.
# Use unofficial, community maintained CMake suite.
%if %{with static_libs}
%cmake -B build-static \
	-DBUILD_SHARED_LIBS=OFF
%{__make} -C build-static
%endif

%cmake -B build

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/src/gtest
cp -pr googletest/{cmake,src,CMakeLists.txt} $RPM_BUILD_ROOT%{_prefix}/src/gtest
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p googletest/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_prefix}/src/gmock
cp -pr googlemock/{cmake,src,CMakeLists.txt} $RPM_BUILD_ROOT%{_prefix}/src/gmock
# gmock CMakeLists.txt expects gtest or ../googletest accessile
ln -snf ../gtest $RPM_BUILD_ROOT%{_prefix}/src/gmock/gtest

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc googletest/README.md
%attr(755,root,root) %{_libdir}/libgtest.so.*.*.*
%attr(755,root,root) %{_libdir}/libgtest_main.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgtest.so
%attr(755,root,root) %{_libdir}/libgtest_main.so
%{_includedir}/gtest
%{_pkgconfigdir}/gtest.pc
%{_pkgconfigdir}/gtest_main.pc
%{_libdir}/cmake/GTest
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgtest.a
%{_libdir}/libgtest_main.a
%endif

%files src
%defattr(644,root,root,755)
%{_prefix}/src/gtest

%files -n gmock
%defattr(644,root,root,755)
%doc googlemock/README.md
%attr(755,root,root) %{_libdir}/libgmock.so.*.*.*
%attr(755,root,root) %{_libdir}/libgmock_main.so.*.*.*

%files -n gmock-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgmock.so
%attr(755,root,root) %{_libdir}/libgmock_main.so
%{_includedir}/gmock
%{_pkgconfigdir}/gmock.pc
%{_pkgconfigdir}/gmock_main.pc

%if %{with static_libs}
%files -n gmock-static
%defattr(644,root,root,755)
%{_libdir}/libgmock.a
%{_libdir}/libgmock_main.a
%endif

%files -n gmock-src
%defattr(644,root,root,755)
%{_prefix}/src/gmock
