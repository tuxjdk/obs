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
# no one should touch our jars, we know better:
%define __jar_repack %{nil}

Name:           netbeans
Version:        8.0.20150708
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
Patch0:         no-javafx-deps.diff

%description
NetBeans IDE is an open-source integrated development environment. 
NetBeans IDE supports development of all Java application types 
(Java SE (including JavaFX), Java ME, web, EJB and mobile applications) 
out of the box. Among other features are an Ant-based project system, 
Maven support, refactorings, version control (supporting CVS, Subversion, 
Git, Mercurial and Clearcase).

%package        ergonomics
Summary:        NetBeans ergonomics suite
Group:          Development/Languages
Requires:       netbeans = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    ergonomics
NetBeans ergonomics suite, adding lazy initialization for all other modules.

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

%package        launchers
Summary:        Path launchers for NetBeans
Group:          Development/Languages
Requires:       netbeans = %{version}
BuildArch:      noarch

%description    launchers
Launch script for NetBeans, located under /usr/local/bin, to be the first
in path but not to conflict with existing jpackage-based packages.

%prep
%setup -q -n %{name}
%patch0 -p1
rm -rf core.browser.webview.jfxplatformbridge  javafx2.editor  javafx2.kit  javafx2.platform  javafx2.project  javafx2.samples  javafx2.scenebuilder  libs.javafx core.browser.webview api.htmlui templatesui
pushd nbbuild
mkdir binaries-cache
pushd binaries-cache
tar -xJf %{SOURCE1}
popd
popd

%build
pushd nbbuild
ant -Dpermit.jdk8.builds=true -Dbinaries.cache="$(pwd)/binaries-cache" -silent build-nozip
popd

%install
##
## CLEANUP START ##
##
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
pushd cvm
rm -rf windows*
popd
popd
# cleaning up files we do not need:
find nbbuild/netbeans -name .lastModified -delete
find nbbuild/netbeans -name *.exe -delete
find nbbuild/netbeans -name *.dll -delete
find nbbuild/netbeans -name *.bat -delete
find nbbuild/netbeans -name *.cmd -delete
rm -f nbbuild/netbeans/nb.cluster.*.built nbbuild/netbeans/*.html nbbuild/netbeans/*.txt nbbuild/netbeans/*.properties nbbuild/netbeans/*.css
# we do not want javafx for now, untill someone will specifically ask for it:
rm -rf nbbuild/netbeans/javafx nbbuild/netbeans/harness/nbi/.common
# fixing end of lines from windows:
sed -i 's/\r$//' nbbuild/netbeans/java/maven/bin/m2.conf
##
## CLEANUP END ##
##
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
/opt/%{name}/apisupport
/opt/%{name}/extra
/opt/%{name}/harness
/opt/%{name}/ide
/opt/%{name}/nb
/opt/%{name}/platform
/opt/%{name}/bin
/opt/%{name}/etc
%attr(755,root,root) /opt/%{name}/bin/*
%attr(755,root,root) /opt/%{name}/harness/launchers/*
%attr(755,root,root) /opt/%{name}/ide/bin/nativeexecution/*.sh
%attr(755,root,root) /opt/%{name}/platform/lib/nbexec
%config /opt/%{name}/etc/*

%files ergonomics
%defattr(644,root,root,755)
%dir /opt/%{name}
/opt/%{name}/ergonomics

%files cnd
%defattr(644,root,root,755)
%dir /opt/%{name}
/opt/%{name}/cnd
/opt/%{name}/cndext
/opt/%{name}/dlight
%attr(755,root,root) /opt/%{name}/cnd/bin/*.sh

%files java
%defattr(644,root,root,755)
%dir /opt/%{name}
/opt/%{name}/extide
/opt/%{name}/java
/opt/%{name}/profiler
%attr(755,root,root) /opt/%{name}/extide/ant/bin/*
%attr(755,root,root) /opt/%{name}/java/maven/bin/*
%attr(644,root,root) /opt/%{name}/java/maven/bin/m2.conf
%attr(755,root,root) /opt/%{name}/profiler/remote-pack-defs/*.sh

%files enterprise
%defattr(644,root,root,755)
%dir /opt/%{name}
/opt/%{name}/enterprise
/opt/%{name}/webcommon
/opt/%{name}/websvccommon

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%changelog
* Wed Jul  8 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build NetBeans.
