%define	fname	tuxtype_w_fonts

Summary:	Educational typing tutor game starring Tux
Name:		tuxtype
Version:	1.8.1
Release:	2
Source0:	%{fname}-%{version}.tar.gz
URL:		http://alioth.debian.org/frs/?group_id=31080
License:	GPLv2+
Group:		Games/Other
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	SDL_Pango-devel
BuildRequires:	imagemagick
BuildRequires:	librsvg-devel
Provides:	tuxtype2 = %{version}-%{release}
Obsoletes:	tuxtype2 < 1.5.3-9

%description 
Tux Typing is an educational typing tutor game starring Tux, the Linux
penguin. It is graphical and requires SDL to run. This is a stable
release.

%prep
%setup -q -n %{fname}-%{version}
# Fix incorrect paths hardcoded into the source (#46417) - AdamW
sed -i -e 's,/usr/share/fonts/truetype/ttf-.*/,%{_gamesdatadir}/%{name}/fonts/,g' src/loaders.c
sed -i -e 's,/usr/share,%{_gamesdatadir},g' src/setup.c

# remove the chown command from here and handle it in the file list
sed -i 's,chown root:games $(DESTDIR)$(pkglocalstatedir)/words,#&,' Makefile.{am,in}

%build
%configure2_5x	--disable-rpath \
		--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir} \
		--localstatedir=%{_localstatedir}/lib \
		--sysconfdir=%{_sysconfdir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -fr %{buildroot}%{_prefix}/doc/tuxtype

install -d %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=TuxType
Comment=Educational typing tutor game starring Tux
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;KidsGame;Educational;
EOF

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 16x16 %{name}.ico %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32x32 %{name}.ico %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 %{name}.ico %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog README doc/en/howtotheme.html
%{_sysconfdir}/%{name}
%{_gamesbindir}/%{name}
%{_datadir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_localstatedir}/lib/%{name}
#% attr(-,root,games) %{_localstatedir}/lib/%{name}/words
