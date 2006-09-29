Summary:	User interface builder for GTK+ and GNOME
Summary(pl):	Budowniczy interfejsów dla GTK+ and GNOME
Name:		glade3
Version:	3.0.2
Release:	1
License:	GPL v2+3B
Group:		Development/Building
Source0:	http://ftp.gnome.org/pub/gnome/sources/glade3/3.0/%{name}-%{version}.tar.bz2
# Source0-md5:	117dd31c908fd32ad7058c9471e21039
Patch0:		%{name}-desktop.patch
URL:		http://glade.gnome.org/
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.10.4
BuildRequires:	libbonoboui-devel >= 2.16.0
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.26
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
Requires:	libgladeui = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Glade is a RAD tool to enable quick & easy development of user
interfaces for the GTK+ toolkit and the GNOME desktop environment.

%description -l pl
Glade jest narzêdziem typu RAD (Rapid Application Development) do
szybkiego i wygodnego tworzenia interfejsu u¿ytkownika opartych
o bibliotekê GTK+ i dla ¶rodowiska biurka GNOME.

%package -n libgladeui
Summary:	libgladeui library
Summary(pl):	Biblioteka libgladeui
Group:		Libraries

%description -n libgladeui
libgladeui library.

%description -n libgladeui -l pl
Biblioteka libgladeui.

%package -n libgladeui-devel
Summary:	Header files for libgladeui library
Summary(pl):	Pliki nag³ówkowe biblioteki libgladeui
Group:		Development/Libraries
Requires:	libgladeui = %{version}-%{release}

%description -n libgladeui-devel
This is the package containing the header files for libgladeui library.

%description -n libgladeui-devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki libgladeui.

%package -n libgladeui-static
Summary:	Static libgladeui library
Summary(pl):	Statyczna biblioteka libgladeui
Group:		Development/Libraries
Requires:	libgladeui-devel = %{version}-%{release}

%description -n libgladeui-static
Static libgladeui library.

%description -n libgladeui-static -l pl
Statyczna biblioteka libgladeui.

%package -n libgladeui-apidocs
Summary:	libgladeui API documentation
Summary(pl):	Dokumentacja API libgladeui
Group:		Documentation
Requires:	gtk-doc-common

%description -n libgladeui-apidocs
libgladeui API documentation.

%description -n libgladeui-apidocs -l pl
Dokumentacja API libgladeui.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/modules/*.{a,la}

%find_lang %{name} --all-name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post	-n libgladeui -p /sbin/ldconfig
%postun -n libgladeui -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%attr(755,root,root) %{_libdir}/%{name}/modules/*.so

%{_datadir}/%{name}
%{_desktopdir}/glade-3.desktop
%{_iconsdir}/hicolor/*/apps/*.png

%files -n libgladeui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-1.so.*.*.*

%files -n libgladeui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgladeui-1.so
%{_libdir}/libgladeui-1.la
%{_includedir}/libgladeui-1.0
%{_pkgconfigdir}/*.pc

%files -n libgladeui-static
%defattr(644,root,root,755)
%{_libdir}/libgladeui-1.a

%files -n libgladeui-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gladeui
