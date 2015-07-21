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

%global vendor  tuxjdk

# who wants to debug the netbeans itself should build it with debug info:
%global debug_package %{nil}
# no one should touch our jars, we know better:
%define __jar_repack %{nil}

Name:           netbeans-beta
Version:        20150721
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
Source3:        netbeans.conf
Source4:        drop-unsupported-modules.sh
Source5:        drop-javadocs.sh
Source6:        post-build-cleanup.sh
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
bash %{SOURCE4}
bash %{SOURCE5}
pushd nbbuild
tar -xJf %{SOURCE1}
popd

%build
pushd nbbuild
ant -Dpermit.jdk8.builds=true -Dbinaries.cache="$(pwd)/binaries-cache" -silent build-nozip
popd

%install
bash %{SOURCE6}
# install config:
cp -f %{SOURCE3} nbbuild/netbeans/etc/
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
# creating main dir:
install -dm 755 %{buildroot}/opt/%{vendor}/%{name}
cp -R nbbuild/netbeans/* %{buildroot}/opt/%{vendor}/%{name}/
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/netbeans
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{vendor}/%{name}/

%files
%defattr(644,root,root,755)
/opt/%{vendor}/%{name}/apisupport
/opt/%{vendor}/%{name}/extra
/opt/%{vendor}/%{name}/harness
/opt/%{vendor}/%{name}/ide
/opt/%{vendor}/%{name}/nb
/opt/%{vendor}/%{name}/platform
/opt/%{vendor}/%{name}/bin
/opt/%{vendor}/%{name}/etc
%attr(755,root,root) /opt/%{vendor}/%{name}/bin/*
%attr(755,root,root) /opt/%{vendor}/%{name}/harness/launchers/*
%attr(755,root,root) /opt/%{vendor}/%{name}/ide/bin/nativeexecution/*.sh
%attr(755,root,root) /opt/%{vendor}/%{name}/platform/lib/nbexec
%config /opt/%{vendor}/%{name}/etc/*

%files ergonomics
%defattr(644,root,root,755)
%dir /opt/%{vendor}/%{name}
/opt/%{vendor}/%{name}/ergonomics

%files cnd
%defattr(644,root,root,755)
%dir /opt/%{vendor}/%{name}
/opt/%{vendor}/%{name}/cnd
/opt/%{vendor}/%{name}/cndext
/opt/%{vendor}/%{name}/dlight
%attr(755,root,root) /opt/%{vendor}/%{name}/cnd/bin/*.sh

%files java
%defattr(644,root,root,755)
%dir /opt/%{vendor}/%{name}
/opt/%{vendor}/%{name}/extide
/opt/%{vendor}/%{name}/java
/opt/%{vendor}/%{name}/profiler
%attr(755,root,root) /opt/%{vendor}/%{name}/extide/ant/bin/*
%attr(755,root,root) /opt/%{vendor}/%{name}/java/maven/bin/*
%attr(644,root,root) /opt/%{vendor}/%{name}/java/maven/bin/m2.conf
%attr(755,root,root) /opt/%{vendor}/%{name}/profiler/remote-pack-defs/*.sh

%files enterprise
%defattr(644,root,root,755)
%dir /opt/%{vendor}/%{name}
/opt/%{vendor}/%{name}/enterprise
/opt/%{vendor}/%{name}/webcommon
/opt/%{vendor}/%{name}/websvccommon

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%changelog
* Tue Jul 21 2015 baiduzhyi.devel@gmail.com
- Initial package for netbeans-beta.
