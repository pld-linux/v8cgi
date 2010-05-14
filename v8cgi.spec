# TODO:
# - scons: *** Path for option v8_path does not exist: ../v8

%define		snap	20100309svn785
%define		svnrev	785
%define		rel		1
Summary:	JavaScript Engine
Name:		v8cgi
Version:	0.8.1
Release:	0.%{svnrev}.%{rel}
License:	BSD
Group:		Libraries
URL:		http://code.google.com/p/v8cgi
# svn co http://v8cgi.googlecode.com/svn/trunk${revno:+@$revno} v8cgi
# tar -cjf v8cgi-$(svnversion v8cgi).tar.bz2 --exclude=.svn v8cgi
# ../dropin v8cgi-$(svnversion v8cgi).tar.bz2 &
# ../md5 v8cgi
Source0:	%{name}-%{svnrev}.tar.bz2
# Source0-md5:	5578247aebd00b5c8a08b0c8b5e3459d
Source1:	%{name}.conf
Patch0:		%{name}-pgsql.patch
BuildRequires:	apache-devel >= 2.2
BuildRequires:	fcgi-devel
BuildRequires:	gcc >= 5:4.0
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	postgresql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	scons
BuildRequires:	v8-devel
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apxs	/usr/sbin/apxs
%define		_apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
Small set of C++ and JS libraries, allowing coder to use JS as a
server-side HTTP processing language. Basic functionality includes IO,
GD, MySQL, Sockets, Templating, FastCGI and Apache module.

%package -n apache-mod_v8cgi
Summary:	Support for v8cgi within Apache
Group:		Networking/Daemons/HTTP
Requires:	apache(modules-api) = %apache_modules_api

%description -n apache-mod_v8cgi
Support for v8cgi within Apache.

%prep
%setup -q -n %{name}
%if "%{pld_release}" == "ac"
%patch0 -p1
%endif

%build
# build library
CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmcflags}"
%if "%{pld_release}" == "ac"
CC="%{__cc}4"
CXX="%{__cxx}4"
%else
CC="%{__cc}"
CXX="%{__cxx}"
%endif
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%scons \
	apache_path=$(apxs -q INCLUDEDIR) \
	cpppath="$(pkg-config --variable=includedir apr-1);$(pkg-config --variable=includedir apr-util-1);%{_includedir}/fastcgi" \
	sockets=1 \
	fcgi=1 \
	mysql=1 \
	pgsql=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/v8cgi,%{_sysconfdir},%{_apacheconfdir},%{_pkglibdir}}
install -p v8cgi $RPM_BUILD_ROOT%{_bindir}/v8cgi
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/v8cgi.conf
install -p lib/* $RPM_BUILD_ROOT%{_libdir}/v8cgi
install mod_v8cgi.so $RPM_BUILD_ROOT%{_pkglibdir}/

echo 'LoadModule %{name}_module	modules/mod_%{name}.so
AddHandler v8cgi-script .ssjs .sjs
v8cgi_Config %{_sysconfdir}/v8cgi.conf' > \
	$RPM_BUILD_ROOT%{_apacheconfdir}/90_mod_%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -n apache-mod_v8cgi
%service -q httpd restart

%postun -n apache-mod_v8cgi
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/v8cgi
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/v8cgi.conf
%dir %{_libdir}/v8cgi
%attr(755,root,root) %{_libdir}/v8cgi/*.so
%{_libdir}/v8cgi/*.js

%files -n apache-mod_v8cgi
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_apacheconfdir}/90_mod_%{name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_v8cgi.so
