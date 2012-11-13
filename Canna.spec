%define	dver	%(echo %{version} | tr -d .)
Summary:	Japanese input system
Summary(ja.UTF-8):	日本語入力システム
Summary(pl.UTF-8):	System wprowadzania znaków japońskich
Name:		Canna
Version:	3.7p3
Release:	4
License:	BSD-like
Group:		Libraries
Source0:	http://downloads.sourceforge.jp/canna/9565/%{name}%{dver}.tar.bz2
# Source0-md5:	0b8c241f63ab4cd3c0b9be569456dc33
Source1:	%{name}.init
Source2:	%{name}-dot-canna
Patch0:		%{name}-conf.patch
Patch1:		%{name}-lib64.patch
URL:		http://canna.sourceforge.jp/
BuildRequires:	cpp
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xorg-cf-files
BuildRequires:	xorg-util-gccmakedep
BuildRequires:	xorg-util-imake
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
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

%description -l ja.UTF-8
Canna は日本語を入力する際に、統一されたユーザインターフェースを提供す
る日本語入力システムです。Nemacs(Mule)、kinput2、canuum をサポートして
います。これらのツールすべては、単一のカスタマイズファイル、ローマ字か
な変換規則、変換辞書を用いて、同様に日本語入力できます。クライアント-
サーバモデルにもとづいてかなを漢字に変換し、逐次的なかな漢字変換をサポー
トしています。

%description -l pl.UTF-8
Canna to system wprowadzania znaków japońskich, dostarczający
jednolity interfejs użytkownika do tego celu. Obsługuje Cemacsa
(Mule), kinput2 i canuum. Wszystkie te narzędzia mogą być używane
poprzez pojedynczy plik konfiguracyjny, w ten sam sposób dla zasad
konwersji romaji do kana, słowników konwersji i wprowadzania znaków.
Canna konwertuje kana do kanji bazując na modelu klient-serwer,
obsługuje też automatyczną konwersję kana do kanji.

%package libs
Summary:	Runtime library for Canna
Summary(pl.UTF-8):	Biblioteki Canna
Group:		Libraries

%description libs
This package contains the runtime library for running programs with
Canna.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki potrzebne do uruchamiania programów
używających Canna.

%package devel
Summary:	Header files for Canna
Summary(pl.UTF-8):	Pliki nagłówkowe Canna
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files for building programs which use
Canna.

%description devel -l ja.UTF-8
このパッケージには Canna を利用したプログラムをコンパイルするために必
要なヘッダファイルとライブラリを含んでいます。

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do budowania programów używających
Canna.

%package static
Summary:	Canna static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Canna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains Canna static libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki Canna.

%prep
%setup -q -n %{name}%{dver}
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

%build
xmkmf -a
%{__make} -j1 canna \
	CC="%{__cc}" \
	CDEBUGFLAGS="%{rpmcflags}" \
	CXXDEBUGFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/skel}

%{__make} -j1 install install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	MANSUFFIX=1 \
	LIBMANSUFFIX=3

xmkmf -a
%{__make} -j1 install.man \
	DESTDIR=$RPM_BUILD_ROOT \
	cannaManDir=%{_mandir} \
	MANSUFFIX=1 \
	LIBMANSUFFIX=3

# convert man symlinks to files
for l in $(find $RPM_BUILD_ROOT%{_mandir} -type l); do
	t=$(readlink $l)
	rm -f $l
	echo ".so $t" > $l
done

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/canna
install %{SOURCE2} $RPM_BUILD_ROOT/etc/skel/.canna

cat > $RPM_BUILD_ROOT%{_sysconfdir}/hosts.canna << EOF
unix
localhost
EOF

rm -rf $RPM_BUILD_ROOT%{_prefix}/man

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- canna < 3.7-p3.3
usermod -d %{_datadir}/canna canna

%pre
%groupadd -g 41 canna
%useradd -u 41 -d %{_datadir}/canna -s /bin/false -c "Canna Service User" -g canna canna

%post
/sbin/chkconfig --add canna
%service canna restart "Canna service"

%preun
if [ "$1" = "0" ]; then
	%service canna stop
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
%doc README WHATIS
%lang(ja) %doc CHANGES.jp README.jp WHATIS.jp
%attr(755,root,root) %{_bindir}/addwords
%attr(755,root,root) %{_bindir}/canlisp
%attr(755,root,root) %{_bindir}/cannacheck
%attr(755,root,root) %{_bindir}/cannastat
%attr(755,root,root) %{_bindir}/catdic
%attr(755,root,root) %{_bindir}/chkconc
%attr(755,root,root) %{_bindir}/chmoddic
%attr(755,root,root) %{_bindir}/cpdic
%attr(755,root,root) %{_bindir}/crfreq
%attr(755,root,root) %{_bindir}/crxdic
%attr(755,root,root) %{_bindir}/crxgram
%attr(755,root,root) %{_bindir}/cshost
%attr(755,root,root) %{_bindir}/ctow
%attr(755,root,root) %{_bindir}/delwords
%attr(755,root,root) %{_bindir}/dicar
%attr(755,root,root) %{_bindir}/dpbindic
%attr(755,root,root) %{_bindir}/dpromdic
%attr(755,root,root) %{_bindir}/dpxdic
%attr(755,root,root) %{_bindir}/forcpp
%attr(755,root,root) %{_bindir}/forsort
%attr(755,root,root) %{_bindir}/kpdic
%attr(755,root,root) %{_bindir}/lsdic
%attr(755,root,root) %{_bindir}/mergeword
%attr(755,root,root) %{_bindir}/mkbindic
%attr(755,root,root) %{_bindir}/mkdic
%attr(755,root,root) %{_bindir}/mkromdic
%attr(755,root,root) %{_bindir}/mvdic
%attr(755,root,root) %{_bindir}/rmdic
%attr(755,root,root) %{_bindir}/splitword
%attr(755,root,root) %{_bindir}/syncdic
%attr(755,root,root) %{_bindir}/wtoc
%attr(755,root,root) %{_sbindir}/cannaserver
%attr(755,root,root) %{_sbindir}/cannakill
%attr(754,root,root) /etc/rc.d/init.d/canna
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hosts.canna
%config(noreplace) %verify(not md5 mtime size) /etc/skel/.canna
%{_mandir}/man1/addwords.1*
%{_mandir}/man1/cannacheck.1*
%{_mandir}/man1/cannakill.1*
%{_mandir}/man1/cannaserver.1*
%{_mandir}/man1/cannastat.1*
%{_mandir}/man1/catdic.1*
%{_mandir}/man1/chmoddic.1*
%{_mandir}/man1/cpdic.1*
%{_mandir}/man1/cshost.1*
%{_mandir}/man1/ctow.1*
%{_mandir}/man1/delwords.1*
%{_mandir}/man1/dicar.1*
%{_mandir}/man1/dpbindic.1*
%{_mandir}/man1/dpromdic.1*
%{_mandir}/man1/lsdic.1*
%{_mandir}/man1/mkbindic.1*
%{_mandir}/man1/mkdic.1*
%{_mandir}/man1/mkromdic.1*
%{_mandir}/man1/mvdic.1*
%{_mandir}/man1/rmdic.1*
%{_mandir}/man1/splitword.1*
%{_mandir}/man1/wtoc.1*
%lang(ja) %{_mandir}/ja/man1/*
%attr(770,root,canna) /var/log/canna

%dir %{_datadir}/canna
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/canna/default.canna
%attr(775,root,canna) %dir %{_datadir}/canna/dic
%attr(664,root,canna) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/canna/dic/*.cbp
%attr(775,root,canna) %dir %{_datadir}/canna/dic/canna
%attr(664,root,canna) %config(noreplace) %verify(not md5 mtime size) %{_datadir}/canna/dic/canna/*.c*
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/canna/dic/canna/dics.dir
%{_datadir}/canna/sample

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libRKC.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libRKC.so.1
%attr(755,root,root) %{_libdir}/libRKC16.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libRKC16.so.1
%attr(755,root,root) %{_libdir}/libcanna.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcanna.so.1
%attr(755,root,root) %{_libdir}/libcanna16.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcanna16.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libRKC.so
%attr(755,root,root) %{_libdir}/libRKC16.so
%attr(755,root,root) %{_libdir}/libcanna.so
%attr(755,root,root) %{_libdir}/libcanna16.so
%{_includedir}/canna
%{_mandir}/man3/Rk*.3*
%{_mandir}/man3/XKanjiControl.3*
%{_mandir}/man3/XLookupKanjiString.3*
%{_mandir}/man3/cannalib.3*
%{_mandir}/man3/jrKanji*.3*
%{_mandir}/man3/uilib.3*
%lang(ja) %{_mandir}/ja/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libRKC.a
%{_libdir}/libRKC16.a
%{_libdir}/libcanna.a
%{_libdir}/libcanna16.a
