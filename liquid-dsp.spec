%global commit 9658d811f9194229304fec2d117f49c59b49a616
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapshotdate 20180806

%define major 1
%define libname	%mklibname liquid-dsp %{major}
%define devname	%mklibname -d liquid-dsp

Name:           liquid-dsp
Version:	1.3.2
Release:	1
Summary:        Digital Signal Processing Library for Software-Defined Radios

License:        MIT
URL:            http://liquidsdr.org/
Source0:        https://github.com/jgaeddert/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# set soname ourselves as upstream doesn't
Patch0:         soname-version.patch
# add autotooling as upstream doesn't
Patch1:         autotools.patch
# fixes ppc64 altivec, other 64-bit problems. Patch by Dan Horák.
# https://github.com/jgaeddert/liquid-dsp/pull/136
Patch2:         ppc64.patch
BuildRequires:  fftw-devel

%description
Digital signal processing library for software-defined radios

%package -n	%{libname}
Summary:	Library for accessing USB devices
Group:		System/Libraries

%description -n	%{libname}
Digital signal processing library for software-defined radios

%package -n %{devname}
Summary:        Development files for %{name}
Requires:       %{libname} = %{EVRD}

%description -n %{devname}
Digital signal processing library for software-defined radios

%prep
%autosetup -p1 -n %{name}-%{commit}
chmod a+x configure

%build
%configure --exec_prefix=/
%make_build

%check
make check

%install
%make_install
pushd ${RPM_BUILD_ROOT}/%{_libdir} > /dev/null 2>&1
rm libliquid.a
ln -s libliquid.so.1.3 libliquid.so
chmod a+x libliquid.so.1.3
popd > /dev/null 2>&1

%files -n %{libname}
%{_libdir}/libliquid.so.%{major}.*

%files -n %{devname}
%license LICENSE
%{_includedir}/liquid/
%{_libdir}/libliquid.so
