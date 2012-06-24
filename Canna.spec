%define	_ver	%(echo %{version} | tr -d .)
%define	_rc		p3
%define	_rel	1
Summary:	Japanese input system
Summary(ja):	���ܸ����ϥ����ƥ�
Summary(pl):	System wprowadzania znak�w japo�skich
Name:		Canna
Version:	3.7
Release:	%{_rc}.%{_rel}
License:	BSD-like
Group:		Libraries
Source0:	http://downloads.sourceforge.jp/canna/9565/%{name}%{_ver}%{_rc}.tar.bz2
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

%description -l ja
Canna �����ܸ�����Ϥ���ݤˡ����줵�줿�桼�����󥿡��ե��������󶡤�
�����ܸ����ϥ����ƥ�Ǥ���Nemacs(Mule)��kinput2��canuum �򥵥ݡ��Ȥ���
���ޤ��������Υġ��뤹�٤Ƥϡ�ñ��Υ������ޥ����ե����롢���޻���
���Ѵ���§���Ѵ�������Ѥ��ơ�Ʊ�ͤ����ܸ����ϤǤ��ޤ������饤�����-
�����Х�ǥ�ˤ�ȤŤ��Ƥ��ʤ�������Ѵ������༡Ū�ʤ��ʴ����Ѵ��򥵥ݡ�
�Ȥ��Ƥ��ޤ���

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
Summary(pl):	Pliki nag��wkowe Canna
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files for building programs which use
Canna.

%description devel -l ja
���Υѥå������ˤ� Canna �����Ѥ����ץ����򥳥�ѥ��뤹�뤿���ɬ
�פʥإå��ե�����ȥ饤�֥���ޤ�Ǥ��ޤ���

%description devel -l pl
Ten pakiet zawiera pliki nag��wkowe do budowania program�w u�ywaj�cych
Canna.

%package static
Summary:	Canna static libraries
Summary(pl):	Biblioteki statyczne Canna
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains Canna static libraries.

%description static -l pl
Ten pakiet zawiera statyczne biblioteki Canna.

%prep
%setup -q -n %{name}%{_ver}%{_rc}
%patch0 -p1
%if "%{_lib}" == "lib64"
%patch1 -p1
%endif

%build
xmkmf -a
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

xmkmf -a
%{__make} install.man \
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
rm -fr $RPM_BUILD_ROOT

%pre
%groupadd -g 41 canna
%useradd -u 41 -d /var/lib/canna -s /bin/false -c "Canna Service User" -g canna canna

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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/cannaserver
%attr(755,root,root) %{_sbindir}/cannakill
%attr(754,root,root) /etc/rc.d/init.d/canna
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hosts.canna
%config(noreplace) %verify(not md5 mtime size) /etc/skel/.canna
%{_mandir}/man1/*
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
%attr(755,root,root) %{_libdir}/libRKC16.so.*.*
%attr(755,root,root) %{_libdir}/libcanna.so.*.*
%attr(755,root,root) %{_libdir}/libcanna16.so.*.*

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
