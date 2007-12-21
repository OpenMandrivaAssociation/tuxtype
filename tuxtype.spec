%define	name	tuxtype
%define	version	1.5.12
%define	release	%mkrel 1

Summary:	Educational typing tutor game starring Tux
Name:		%{name}
Version:	%{version}
Release:	%{release}
# have to change with each new release as the number after download.php changes :(
Source0:	http://alioth.debian.org/frs/download.php/2136/%{name}-%{version}.tar.gz
URL:		http://alioth.debian.org/frs/?group_id=31080
License:	GPLv2+
Group:		Games/Other
BuildRequires:	SDL-devel SDL_ttf-devel SDL_mixer-devel SDL_image-devel SDL_Pango-devel
BuildRequires:	ImageMagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:	tuxtype2
Obsoletes:	tuxtype2

%description 
Tux Typing is an educational typing tutor game starring Tux, the Linux
penguin. It is graphical and requires SDL to run. This is a stable
release.

%prep
%setup -q

%build
%configure	--bindir=%{_gamesbindir} \
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

%post
%{update_menus}
%update_icon_cache hicolor

%postun
%{clean_menus}
%clean_icon_cache hicolor

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README tuxtype/docs/en/howtotheme.html 
%{_gamesbindir}/tuxtype
%{_datadir}/tuxtype
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

