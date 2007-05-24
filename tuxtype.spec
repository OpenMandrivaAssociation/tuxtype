%define	name	tuxtype
%define	version	1.5.8
%define	release	%mkrel 1
%define	Summary	Educational typing tutor game starring Tux

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
# have to change with each new release as the number after download.php changes :(
Source0:	http://alioth.debian.org/frs/download.php/1953/%{name}-%{version}.tar.bz2
URL:		http://alioth.debian.org/frs/?group_id=31080
License:	GPL 
Group:		Games/Other
BuildRequires:	SDL-devel SDL_ttf-devel SDL_mixer-devel SDL_image-devel
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

mkdir -p %{buildroot}%{_menudir}
cat << EOF > $RPM_BUILD_ROOT/%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" \
	icon="%{name}.png" \
	needs="x11" \
	section="More Applications/Games/Other" \
	title="TuxType" \
	longtitle="%{Summary}" \
	xdg="true"
EOF

install -d %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Encoding=UTF-8
Name=TuxType2
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;KidsGame;Educational;X-MandrivaLinux-MoreApplications-Games-Other;
EOF

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
convert -scale 16x16 %{name}.ico %{buildroot}%{_miconsdir}/%{name}.png
convert -scale 32x32 %{name}.ico %{buildroot}%{_iconsdir}/%{name}.png
convert -scale 48x48 %{name}.ico %{buildroot}%{_liconsdir}/%{name}.png

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
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
