%define major 8
%define libname %mklibname jpeg %{major}
%define develname %mklibname -d jpeg
%define staticname %mklibname -s -d jpeg

Summary:	A library for manipulating JPEG image format files
Name:		libjpeg
Version:	8
Release:	%mkrel 3
License:	GPL-like
Group:		System/Libraries
URL:		http://www.ijg.org/
Source0:	ftp://ftp.uu.net/graphics/jpeg/jpegsrc.v8.tar.gz
# Modified source files for lossless cropping of JPEG files and for
# lossless pasting of one JPEG into another (dropping). In addition a
# bug in the treatment of EXIF data is solved and the EXIF data is
# adjusted according to size/dimension changes caused by rotating and
# cropping operations
Source1:	http://jpegclub.org/droppatch.tar.bz2
# These two allow automatic lossless rotation of JPEG images from a digital
# camera which have orientation markings in the EXIF data. After rotation
# the orientation markings are reset to avoid duplicate rotation when
# applying these programs again.
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
Patch0:		jpeg-6b-c++fixes.patch
Patch1:		jpeg-7-missing_arithmetic_functions.diff
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libjpeg package contains a shared library of functions for loading,
manipulating and saving JPEG format image files.

Install the libjpeg package if you need to manipulate JPEG files. You
should also install the jpeg-progs package.

%package -n	%{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n	%{develname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	jpeg-devel = %{version}-%{release}
Provides:	jpeg%{major}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Conflicts:	jpeg6-devel
Obsoletes:	%{mklibname jpeg 62 -d} < 6b-45
Obsoletes:	%{mklibname jpeg 7 -d} < 7-3

%description -n	%{develname}
The libjpeg-devel package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	%{staticname}
Summary:	Static libraries for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Provides:	jpeg-static-devel = %{version}-%{release}
Provides:	jpeg%{major}-static-devel = %{version}-%{release}
Conflicts:	jpeg6-static-devel
Obsoletes:	%{mklibname jpeg 62 -d -s} < 6b-45
Obsoletes:	%{mklibname jpeg 7 -d -s} < 7-3

%description -n	%{staticname}
The libjpeg-devel package includes the static librariesnecessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package -n	jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
Requires:	%{libname} = %{version}-%{release}
Provides:	jpeg-progs = %{version}-%{release}
Provides:	libjpeg-progs = %{version}-%{release}
Obsoletes:	libjpeg-progs

%description -n	jpeg-progs
The jpeg-progs package contains simple client programs for accessing 
the libjpeg functions.  Libjpeg client programs include cjpeg, djpeg, 
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into JPEG
format. Djpeg decompresses a JPEG file into a regular image file.  Jpegtran
can perform various useful transformations on JPEG files.  Rdjpgcom displays
any text comments included in a JPEG file.  Wrjpgcom inserts text
comments into a JPEG file.

%prep

%setup -q -n jpeg-8 -a1
rm -f jpegtran
%patch0 -p0
%patch1 -p0

cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%build
%configure2_5x \
    --disable-silent-rules \
    --enable-shared \
    --enable-static

%make

gcc %{optflags} -o jpegexiforient jpegexiforient.c

LD_PRELOAD=$PWD/.libs/%{name}.so make test

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

#(neoclust) Provide jpegint.h because it is needed softwares
cp jpegint.h %{buildroot}%{_includedir}/jpegint.h

%makeinstall mandir=%{buildroot}%{_mandir}

install -m 755 jpegexiforient %{buildroot}%{_bindir}
install -m 755 exifautotran %{buildroot}%{_bindir}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README change.log coderules.txt filelist.txt install.txt jconfig.txt libjpeg.txt structure.txt usage.txt wizard.txt
%{_libdir}/libjpeg.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc example.c
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/*.la

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/*.a

%files -n jpeg-progs
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
