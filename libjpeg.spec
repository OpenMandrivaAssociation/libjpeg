%define major	9
%define libname	%mklibname jpeg %{major}
%define devname	%mklibname -d jpeg

Summary:	A library for manipulating JPEG image format files
Name:		libjpeg
Version:	9
Release:	1
License:	GPL-like
Group:		System/Libraries
Url:		http://www.ijg.org/
Source0:	http://www.ijg.org/files/jpegsrc.v9.tar.gz
# Modified source files for lossless cropping of JPEG files and for
# lossless pasting of one JPEG into another (dropping). In addition a
# bug in the treatment of EXIF data is solved and the EXIF data is
# adjusted according to size/dimension changes caused by rotating and
# cropping operations
Source1:	http://jpegclub.org/droppatch.v8.tar.gz
# These two allow automatic lossless rotation of JPEG images from a digital
# camera which have orientation markings in the EXIF data. After rotation
# the orientation markings are reset to avoid duplicate rotation when
# applying these programs again.
Source2:	http://jpegclub.org/jpegexiforient.c
Source3:	http://jpegclub.org/exifautotran.txt
Patch0:		jpeg-6b-c++fixes.patch
Patch1:		jpeg-8d-borkfix.diff
BuildRequires:	libtool

%description
The libjpeg package contains a shared library of functions for loading,
manipulating and saving JPEG format image files.

%package -n %{libname}
Summary:	A library for manipulating JPEG image format files
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libjpeg.

%package -n %{devname}
Summary:	Development tools for programs which will use the libjpeg library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	jpeg-devel = %{version}-%{release}
Provides:	jpeg%{major}-devel = %{version}-%{release}
Conflicts:	jpeg6-devel
Obsoletes:	%{mklibname jpeg 62 -d} < 6b-45

%description -n	%{devname}
This package includes the header files necessary for 
developing programs which will manipulate JPEG files using
the libjpeg library.

%package -n jpeg-progs
Summary:	Programs for manipulating JPEG format image files
Group:		Graphics
Provides:	jpeg-progs = %{version}-%{release}

%description -n	jpeg-progs
The jpeg-progs package contains simple client programs for accessing 
the libjpeg functions.  Libjpeg client programs include cjpeg, djpeg, 
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into JPEG
format. Djpeg decompresses a JPEG file into a regular image file.  Jpegtran
can perform various useful transformations on JPEG files.  Rdjpgcom displays
any text comments included in a JPEG file.  Wrjpgcom inserts text
comments into a JPEG file.

%prep
%setup -qn jpeg-9 -a1
rm -f jpegtran
%patch0 -p0
%patch1 -p0

cp %{SOURCE2} jpegexiforient.c
cp %{SOURCE3} exifautotran

%build
%configure2_5x \
	--disable-silent-rules \
	--enable-shared \
	--disable-static

%make

gcc %{optflags} -o jpegexiforient jpegexiforient.c

LD_PRELOAD=$PWD/.libs/%{name}.so make test

%install
mkdir -p %{buildroot}/{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man1}

#(neoclust) Provide jpegint.h because it is needed softwares
cp jpegint.h %{buildroot}%{_includedir}/jpegint.h

%makeinstall mandir=%{buildroot}%{_mandir}

install -m 755 jpegexiforient %{buildroot}%{_bindir}
install -m 755 exifautotran %{buildroot}%{_bindir}

%files -n %{libname}
%{_libdir}/libjpeg.so.%{major}*

%files -n %{devname}
%doc example.c README change.log coderules.txt filelist.txt install.txt jconfig.txt libjpeg.txt structure.txt usage.txt wizard.txt
%{_libdir}/*.so
%{_includedir}/*.h

%files -n jpeg-progs
%{_bindir}/*
%{_mandir}/man1/*

