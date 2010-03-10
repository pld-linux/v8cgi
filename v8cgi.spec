
%define		snap	20100309svn785
%define		rel		1
Summary:	JavaScript Engine
Name:		v8cgi
Version:	0.8.1
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Libraries
URL:		http://code.google.com/p/v8cgi
# No tarballs, pulled from svn
# svn export http://v8cgi.googlecode.com/svn/trunk/ v8cgi
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	3f7d283316c8e39ae3abd64b5c09ffd7
Source1:	%{name}.conf
BuildRequires:	gcc >= 4.0
BuildRequires:	libstdc++-devel
BuildRequires:	scons
BuildRequires:	v8-devel
BuildRequires:	xerces-c-devel
ExclusiveArch:	%{ix86} %{x8664} arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Small set of C++ and JS libraries, allowing coder to use JS as a server-side
HTTP processing language. Basic functionality includes IO, GD, MySQL,
Sockets, Templating, FastCGI and Apache module.

%prep
%setup -q -n %{name}

%build
# build library

CFLAGS="%{rpmcflags}"
CXXFLAGS="%{rpmcxxflags}"
LDFLAGS="%{rpmcflags}"
%if "%{pld_release}" == "ac"
CC=%{__cc}4
CXX=%{__cxx}4
%else
CC=%{__cc}
CXX=%{__cxx}
%endif
export CFLAGS LDFLAGS CXXFLAGS CC CXX
%scons \
	apache_path=`apxs -q INCLUDEDIR` \
	cpppath=`pkg-config --variable=includedir apr-1`\;`pkg-config --variable=includedir apr-util-1`\;/usr/include/fastcgi \
	sockets=1 \
	xdom=1 \
	fcgi=1 \
	mysql=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/v8cgi,%{_sysconfdir}}
install -p v8cgi $RPM_BUILD_ROOT%{_bindir}/v8cgi
install $SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/v8cgi.conf
install lib/* $RPM_BUILD_ROOT%{_libdir}/v8cgi/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/v8cgi
%dir %{_libdir}/v8cgi
%attr(755,root,root) %{_libdir}/v8cgi/*.so
%{_libdir}/v8cgi/*.js
