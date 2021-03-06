# TODO: gnome and python modules to subpackages?
#
# Conditional build:
%bcond_without	gnome	# GNOME catalog support
%bcond_without	python	# Python catalog support

Summary:	User interface builder for GTK+ and GNOME
Summary(pl.UTF-8):	Budowniczy interfejsów dla GTK+ i GNOME
Name:		glade3
Version:	3.8.6
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glade3/3.8/%{name}-%{version}.tar.xz
# Source0-md5:	c16756952967f7316d64593124761027
Patch0:		lib64.patch
URL:		http://glade.gnome.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	gnome-common
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.0
%{?with_gnome:BuildRequires:	libbonoboui-devel >= 2.24.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.24.0}
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-pygtk-devel >= 2:2.14.0}
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	libgladeui = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glade is a RAD tool to enable quick & easy development of user
interfaces for the GTK+ toolkit and the GNOME desktop environment.

%description -l pl.UTF-8
Glade jest narzędziem typu RAD (Rapid Application Development) do
szybkiego i wygodnego tworzenia interfejsu użytkownika opartych o
bibliotekę GTK+ i dla środowiska biurka GNOME.

%package -n libgladeui
Summary:	libgladeui - Glade interface designer library
Summary(pl.UTF-8):	Biblioteka libgladeui do projektowania interfejsu Glade
Group:		X11/Libraries
Requires:	gtk+2 >= 2:2.24.0
Requires:	libxml2 >= 1:2.6.31

%description -n libgladeui
libgladeui - Glade interface designer library.

%description -n libgladeui -l pl.UTF-8
Biblioteka libgladeui do projektowania interfejsu Glade.

%package -n libgladeui-devel
Summary:	Header files for libgladeui library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgladeui
Group:		X11/Development/Libraries
Requires:	gtk+2-devel >= 2:2.24.0
Requires:	libgladeui = %{version}-%{release}
Requires:	libxml2-devel >= 1:2.6.31

%description -n libgladeui-devel
This is the package containing the header files for libgladeui
library.

%description -n libgladeui-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libgladeui.

%package -n libgladeui-static
Summary:	Static libgladeui library
Summary(pl.UTF-8):	Statyczna biblioteka libgladeui
Group:		X11/Development/Libraries
Requires:	libgladeui-devel = %{version}-%{release}

%description -n libgladeui-static
Static libgladeui library.

%description -n libgladeui-static -l pl.UTF-8
Statyczna biblioteka libgladeui.

%package -n libgladeui-apidocs
Summary:	libgladeui API documentation
Summary(pl.UTF-8):	Dokumentacja API libgladeui
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description -n libgladeui-apidocs
libgladeui API documentation.

%description -n libgladeui-apidocs -l pl.UTF-8
Dokumentacja API libgladeui.

%prep
%setup -q
%patch0 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON_LIBS="-lpython" \
	PYTHON_LIB_LOC="%{_libdir}" \
	%{!?with_gnome:--disable-gnome} \
	--enable-gtk-doc \
	%{!?with_python:--disable-python} \
	--disable-scrollkeeper \
	--disable-silent-rules \
	--enable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/glade3/modules/*.{a,la} \
	$RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name} --all-name --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%post	-n libgladeui -p /sbin/ldconfig
%postun -n libgladeui -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
# COPYING contains just general notes (license texts are in COPYING.{GPL,LGPL})
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/glade-3
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%if %{with gnome}
%attr(755,root,root) %{_libdir}/%{name}/modules/libgladegnome.so
%endif
%attr(755,root,root) %{_libdir}/%{name}/modules/libgladegtk.so
%if %{with python}
%attr(755,root,root) %{_libdir}/%{name}/modules/libgladepython.so
%endif
%{_datadir}/%{name}
%{_desktopdir}/glade-3.desktop
%{_iconsdir}/hicolor/*/apps/glade-3.png
%{_iconsdir}/hicolor/*/apps/glade-3.svg

%files -n libgladeui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgladeui-1.so.11

%files -n libgladeui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-1.so
%{_includedir}/libgladeui-1.0
%{_pkgconfigdir}/gladeui-1.0.pc

%files -n libgladeui-static
%defattr(644,root,root,755)
%{_libdir}/libgladeui-1.a

%files -n libgladeui-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gladeui
