# Non-trivial to fix error with this enabled, code doesn't look
# dangerous - AdamW 2008/12
%define Werror_cflags	%nil

%define	fname	tuxtype_w_fonts

Summary:	Educational typing tutor game starring Tux
Name:		tuxtype
Version:	1.7.4
Release:	%{mkrel 1}
# have to change with each new release as the number after download.php changes :(
Source0:	http://alioth.debian.org/frs/download.php/2686/%{fname}-%{version}.tar.gz
URL:		http://alioth.debian.org/frs/?group_id=31080
License:	GPLv2+
Group:		Games/Other
BuildRequires:	SDL-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_Pango-devel
BuildRequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
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

%build
%configure2_5x	--bindir=%{_gamesbindir} \
		--datadir=%{_gamesdatadir}
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

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog README doc/en/howtotheme.html 
%{_gamesbindir}/%{name}
%{_datadir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

