#
# spec file for package netbeans
#
# Copyright (c) 2015 Stanislav Baiduzhyi <baiduzhyi.devel@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


# who wants to debug the netbeans itself should build it with debug info:
%global debug_package %{nil}
%define __jar_repack %{nil}

Name:           netbeans
Version:        8.0.2.20150702
Release:        0
URL:            http://www.netbeans.org/
Summary:        Integrated development environment
License:        CDDL-1.0
Group:          Development/Languages
BuildArch:      noarch
AutoReqProv:    no
BuildRequires:  bash
BuildRequires:  tuxjdk
BuildRequires:  ant-launchers
BuildRequires:  fdupes
Requires:       tuxjdk
Source0:        %{name}.tar.xz
Source1:        binaries-cache.tar.xz
Source2:        %{name}-launcher.sh
Source3:        %{name}.conf
Source10:       netbeans-rpmlintrc

%description
NetBeans IDE is an open-source integrated development environment. 
NetBeans IDE supports development of all Java application types 
(Java SE (including JavaFX), Java ME, web, EJB and mobile applications) 
out of the box. Among other features are an Ant-based project system, 
Maven support, refactorings, version control (supporting CVS, Subversion, 
Git, Mercurial and Clearcase).

%package        launchers
Summary:        Path launchers for NetBeans
Group:          Development/Languages
Requires:       netbeans = %{version}
BuildArch:      noarch

%description    launchers
Launch script for NetBeans, located under /usr/local/bin, to be the first
in path but not to conflict with existing jpackage-based packages.

%package        cnd
Summary:        C/C++ development for NetBeans
Group:          Development/Languages
Requires:       netbeans = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    cnd
C/C++ development environment for NetBeans.

%package        java
Summary:        Java development for NetBeans
Group:          Development/Languages
Requires:       netbeans = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    java
Java development environment for NetBeans.

%package        enterprise
Summary:        Enterprise Java development for NetBeans
Group:          Development/Languages
Requires:       netbeans-java = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    enterprise
Enterprise Java development environment for NetBeans.

%prep
%setup -q -n %{name}
pushd nbbuild
mkdir binaries-cache
pushd binaries-cache
tar -xJf %{SOURCE1}
popd
echo 'permit.jdk8.builds=true' >user.build.properties
echo "binaries.cache=$(pwd)/binaries-cache" >>user.build.properties
popd

%build
pushd nbbuild
ant -silent build-nozip
ant -silent build-nozip
popd

%install
# cleaning up non-linux stuff:
pushd nbbuild/netbeans/ide/bin/nativeexecution
rm -rf Sun* Mac* Windows*
popd
pushd nbbuild/netbeans/profiler/lib/deployed
pushd jdk15
rm -rf hpux* mac solaris* windows*
popd
pushd jdk16
rm -rf hpux* mac solaris* windows*
popd
popd
# cleaning up files we do not need:
find nbbuild/netbeans -name .lastModified -delete
find nbbuild/netbeans -name *.exe -delete
rm -f nbbuild/netbeans/nb.cluster.*.built nbbuild/netbeans/*.html nbbuild/netbeans/*.txt nbbuild/netbeans/*.properties nbbuild/netbeans/*.css
# we do not want javafx for now, untill someone will specifically ask for it:
rm -rf nbbuild/netbeans/javafx
# setting executable flags:
find nbbuild/netbeans -name *.sh -exec chmod a+x {} +
find nbbuild/netbeans -name *.py -exec chmod a+x {} +
chmod a+x nbbuild/netbeans/bin/netbeans
# install config:
cp -f %{SOURCE3} nbbuild/netbeans/etc/
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
# creating main dir:
install -dm 755 %{buildroot}/opt/%{name}
cp -R nbbuild/netbeans/* %{buildroot}/opt/%{name}/
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/netbeans
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{name}/

%files
%defattr(644,root,root,755)
%attr(755,root,root) /opt/%{name}/bin/*
%config /opt/%{name}/etc/*
/opt/%{name}/extide
/opt/%{name}/harness
/opt/%{name}/ide
/opt/%{name}/nb
/opt/%{name}/platform

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%files cnd
%defattr(755,root,root,755)
%dir /opt/%{name}
/opt/%{name}/cnd
/opt/%{name}/dlight

%files java
%defattr(755,root,root,755)
%dir /opt/%{name}
/opt/%{name}/java
/opt/%{name}/profiler

%files enterprise
%defattr(755,root,root,755)
%dir /opt/%{name}
/opt/%{name}/enterprise
/opt/%{name}/webcommon
/opt/%{name}/websvccommon

%changelog
* Wed Jul  1 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build NetBeans.
