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
# we are bundling some pre-built binaries, should not fail on them:
%global _binaries_in_noarch_packages_terminate_build 0

Name:           netbeans
Version:        8.1.0.21
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
%if 0%{?suse_version}
BuildRequires:  update-desktop-files
%endif
Requires:       tuxjdk
Source0:        %{name}.tar.xz
Source1:        binaries-cache.tar.xz
Source2:        %{name}-launcher.sh
Source3:        netbeans.conf
Source4:        %{name}.desktop
Source11:       nb40.png
Source12:       nb40.icns
Source13:       nb40_16.gif
Source14:       nb40_32.gif
Source15:       nb40_48.gif
Source91:       drop-unsupported-modules.sh
Source92:       drop-javadocs.sh
Source93:       tuxjdk-change-default-font-size.sh
Source94:       drop-jre-splash.sh
Source99:       post-build-cleanup.sh
Source100:      netbeans-rpmlintrc

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
Requires:       %{name} = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    ergonomics
NetBeans ergonomics suite, adding lazy initialization for all other modules.

%package        cnd
Summary:        C/C++ development for NetBeans
Group:          Development/Languages
Requires:       %{name} = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    cnd
C/C++ development environment for NetBeans.

%package        java
Summary:        Java development for NetBeans
Group:          Development/Languages
Requires:       %{name} = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    java
Java development environment for NetBeans.

%package        enterprise
Summary:        Enterprise Java development for NetBeans
Group:          Development/Languages
Requires:       %{name}-java = %{version}
BuildArch:      noarch
AutoReqProv:    no

%description    enterprise
Enterprise Java development environment for NetBeans.

%package        launchers
Summary:        Path launchers for NetBeans
Group:          Development/Languages
Requires:       %{name} = %{version}
BuildArch:      noarch

%description    launchers
Launch script for NetBeans, located under /usr/local/bin, to be the first
in path but not to conflict with existing jpackage-based packages.

%prep
%setup -q -n %{name}
## dropping everything javafx related,
## openjdk does not have the support for javafx
## and we are not interested in maintaining it anyway:
bash %{SOURCE91}
## we do not need javadocs now,
## and because of javafx modules drop some of them
## are not even buildable:
bash %{SOURCE92}
## tuxjdk solves the 'pt' inconsistency of openjdk,
## so we want default size of 9 instead of 13:
bash %{SOURCE93}
## using good old NetBeans 4.1 icons:
cp -f %{SOURCE11} ide.branding/release/netbeans.png
cp -f %{SOURCE12} ide.branding/release/netbeans.icns
cp -f %{SOURCE13} ide.branding/core.startup/src/org/netbeans/core/startup/frame_nb.gif
cp -f %{SOURCE14} ide.branding/core.startup/src/org/netbeans/core/startup/frame32_nb.gif
cp -f %{SOURCE15} ide.branding/core.startup/src/org/netbeans/core/startup/frame48_nb.gif
## unpacking binary build dependencies:
pushd nbbuild
tar -xJf %{SOURCE1}
popd

%build
pushd nbbuild
export ANT_OPTS='-Xmx2G'
ant -Dpermit.jdk8.builds=true -Dbinaries.cache="$(pwd)/binaries-cache" -silent build-nozip
popd

%install
## awt splash screen has an issue with xinerama:
## https://bugs.openjdk.java.net/browse/JDK-6481523
## but NetBeans splash screen works very well,
## so we will sed out the '-splash:smthng' argument
## from netbeans startup scripts:
bash %{SOURCE94}
## remove all the windows and mac libraries and scripts,
## hidden files and everything that we do not want to distribute
## after the build:
bash %{SOURCE99}
# install config:
cp -f %{SOURCE3} nbbuild/netbeans/etc/
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
# creating main dir:
install -dm 755 %{buildroot}/opt/%{vendor}/%{name}
cp -R nbbuild/netbeans/* %{buildroot}/opt/%{vendor}/%{name}/
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/%{name}
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{vendor}/%{name}/
%if 0%{?suse_version}
# desktop file:
%suse_update_desktop_file -i %{name} Development IDE
%else
install -Dm 0644 %{SOURCE4} %{buildroot}/usr/share/applications/%{name}.desktop
%endif

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
%{_datadir}/applications/%{name}.desktop

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
