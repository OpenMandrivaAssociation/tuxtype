%define	fname	tuxtype_w_fonts

Summary:	Educational typing tutor game starring Tux
Name:		tuxtype
Version:	1.5.17
Release:	%{mkrel 1}
# have to change with each new release as the number after download.php changes :(
Source0:	http://alioth.debian.org/frs/download.php/2370/%{fname}-%{version}.tar.gz
URL:		http://alioth.debian.org/frs/?group_id=31080
License:	GPLv2+
Group:		Games/Other
BuildRequires:	SDL-devel SDL_ttf-devel SDL_mixer-devel SDL_image-devel SDL_Pango-devel
BuildRequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	tuxtype2
Obsoletes:	tuxtype2

%description 
Tux Typing is an educational typing tutor game starring Tux, the Linux
penguin. It is graphical and requires SDL to run. This is a stable
release.

%prep
%setup -q -n %{fname}-%{version}

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

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README tuxtype/docs/en/howtotheme.html 
%{_gamesbindir}/%{name}
%{_datadir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

