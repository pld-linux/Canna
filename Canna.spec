Summary:	Japanese input system
Summary(ja):	日本語入力システム
Summary(pl):	System wprowadzania znak�w japo�skich
Name:		Canna
Version:	3.5b2
Release:	44
License:	BSD-like
Group:		Libraries
#origin, but host not found: ftp://ftp.nec.co.jp/pub/Canna/Canna35/Canna35b2.tar.gz
Source0:	ftp://ftp.tokyonet.ad.jp/pub/misc/%{name}/%{name}35/%{name}35b2.tar.gz
# Source0-md5:	09ae4dd3a5d33168ba17470ad9242cf3
Source1:	%{name}.init
Source2:	%{name}-dot-canna
Patch0:		%{name}-conf.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-stdin.patch
Patch4:		%{name}-bcopy.patch
Patch5:		%{name}-security.patch
Patch6:		%{name}-hosts.canna-fix.patch
Patch7:		%{name}-nonstrip.patch
Patch8:		%{name}-wconv.patch
Patch9:		%{name}-multivul.patch
Patch10:	%{name}-fixes.patch
URL:		http://www.nec.co.jp/japanese/product/computer/soft/canna/
BuildRequires:	imake
BuildRequires:	rpmbuild(macros) >= 1.202
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	%{name}-libs = %{version}
Provides:	group(canna)
Provides:	user(canna)
ExcludeArch:	ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Canna is a Japanese input system and provides a unified user interface
for inputing Japanese. It supports Nemacs(Mule), kinput2, and canuum.
All of these tools can be used by a single customization file,
romaji-to-kana conversion rules and conversion dictionaries, and input
Japanese in the same way. It converts kana to kanji based on a
client-server model and supports automatically kana-to-kanji
conversion.

%description -l ja
Canna は日本語を入力する際に、統一されたユーザインターフェースを提供す
る日本語入力システムです。Nemacs(Mule)、kinput2、canuum をサポートして
います。これらのツールすべては、単一のカスタマイズファイル、ローマ字か
な変換規則、変換辞書を用いて、同様に日本語入力できます。クライアント-
サーバモデルにもとづいてかなを漢字に変換し、逐次的なかな漢字変換をサポー
トしています。

%description -l pl
Canna to system wprowadzania znak�w japo�skich, dostarczaj�cy
jednolity interfejs u�ytkownika do tego celu. Obs�uguje Cemacsa
(Mule), kinput2 i canuum. Wszystkie te narz�dzia mog� by� u�ywane
poprzez pojedynczy plik konfiguracyjny, w ten sam spos�b dla zasad
konwersji romaji do kana, s�ownik�w konwersji i wprowadzania znak�w.
Canna konwertuje kana do kanji bazuj�c na modelu klient-serwer,
obs�uguje te� automatyczn� konwersj� kana do kanji.

%package libs
Summary:	Runtime library for Canna
Summary(pl):	Biblioteki Canna
Group:		Libraries

%description libs
This package contains the runtime library for running programs with
Canna.

%description libs -l pl
Ten pakiet zawiera biblioteki potrzebne do uruchamiania program�w
u�ywaj�cych Canna.

%package devel
Summary:	Header files for Canna
Summary(pl):	Pliki nag鞄wkowe Canna
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description devel
This package contains the header files for building programs which use
Canna.

%description devel -l ja
このパッケージには Canna を利用したプログラムをコンパイルするために必
要なヘッダファイルとライブラリを含んでいます。

%description devel -l pl
Ten pakiet zawiera pliki nag鞄wkowe do budowania program�w u�ywaj�cych
Canna.

%package static
Summary:	Canna static libraries
Summary(pl):	Biblioteki statyczne Canna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This package contains Canna static libraries.

%description static -l pl
Ten pakiet zawiera statyczne biblioteki Canna.

%prep
%setup -q -n %{name}35b2
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch2 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p2
%patch8 -p1
%patch9 -p1
%patch10 -p1

%{__perl} -pi -e 's@/usr/lib$@%{_libdir}@' Canna.conf

%build
xmkmf -a
# by some reason sglobal.h is not made automatically - workaround:
%{__make} sglobal.h -C lib/canna
%{__make} canna \
	CDEBUGFLAGS="%{rpmcflags}" \
	CXXDEBUGFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/skel}

%{__make} install install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	MANSUFFIX=1 \
	LIBMANSUFFIX=3

# default manuals are in Japanese; install English ones too
mv -f Canna.conf Canna.conf.orig
sed -e 's/^#define JAPANESEMAN.*//' Canna.conf.orig > Canna.conf
xmkmf -a
%{__make} install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	cannaManDir=%{_mandir} \
	MANSUFFIX=1 \
	LIBMANSUFFIX=3

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/canna
install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.canna

cat > $RPM_BUILD_ROOT%{_sysconfdir}/hosts.canna << EOF
unix
localhost
EOF

%clean
rm -fr $RPM_BUILD_ROOT

%pre
%groupadd -g 41 canna
%useradd -u 41 -d /var/lib/canna -s /bin/false -c "Canna Service User" -g canna canna

%post
/sbin/chkconfig --add canna
if [ -f /var/lock/subsys/canna ]; then
	/etc/rc.d/init.d/canna restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/canna start\" to start Canna service."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/canna ]; then
		/etc/rc.d/init.d/canna stop 1>&2
	fi
	/sbin/chkconfig --del canna
fi

%postun
if [ "$1" = "0" ]; then
	%userremove canna
	%groupremove canna
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README WHATIS doc
%lang(ja) %doc CHANGES.jp README.jp WHATIS.jp
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/cannaserver
%attr(755,root,root) %{_sbindir}/cannakill
%attr(754,root,root) /etc/rc.d/init.d/canna
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/hosts.canna
%config(noreplace) %verify(not size mtime md5) /etc/skel/.canna
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%attr(770,root,canna) /var/log/canna
%dir /var/lib/canna
%config(noreplace) %verify(not size mtime md5) /var/lib/canna/default.canna
%config(noreplace) %verify(not size mtime md5) /var/lib/canna/engine.cf
%attr(775,root,canna) %dir /var/lib/canna/dic
%attr(664,root,canna) %config(noreplace) %verify(not size mtime md5) /var/lib/canna/dic/*.cbp
%attr(775,root,canna) %dir /var/lib/canna/dic/canna
%attr(664,root,canna) %config(noreplace) %verify(not size mtime md5) /var/lib/canna/dic/canna/*.c*
%config(noreplace) %verify(not size mtime md5) /var/lib/canna/dic/canna/dics.dir
/var/lib/canna/sample

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libRKC.so.1.0.0
%attr(755,root,root) %{_libdir}/libRKC16.so.1.0.0
%attr(755,root,root) %{_libdir}/libcanna.so.1.0.0
%attr(755,root,root) %{_libdir}/libcanna16.so.1.0.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libRKC.so
%attr(755,root,root) %{_libdir}/libRKC16.so
%attr(755,root,root) %{_libdir}/libcanna.so
%attr(755,root,root) %{_libdir}/libcanna16.so
%{_includedir}/canna
%{_mandir}/man3/*
%lang(ja) %{_mandir}/ja/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libRKC.a
%{_libdir}/libRKC16.a
%{_libdir}/libcanna.a
%{_libdir}/libcanna16.a
