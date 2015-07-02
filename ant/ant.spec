#
# spec file for package ant
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


# openjdk build system is different,
# we are building release so there is no useful debuginfo,
# so disabling debuginfo package creation:
%global debug_package %{nil}
%define __jar_repack %{nil}

Name:           ant
Version:        1.9.5
Release:        0
URL:            http://ant.apache.org/
Summary:        Java library and command-line tool that help building software
License:        Apache-2.0
Group:          Development/Languages
BuildArch:      noarch
BuildRequires:  bash
BuildRequires:  tuxjdk
BuildRequires:  fdupes
Source0:        apache-ant-%{version}-src.tar.bz2
Source1:        ant-optional-libs.tar.xz
Source2:        ant-launcher.sh

%description
Apache Ant is a Java library and command-line tool that help building software.

%package        launchers
Summary:        Path launchers for Ant
Group:          Development/Languages
Requires:       ant = %{version}
BuildArch:      noarch

%description    launchers
Launch script for Ant, located under /usr/local/bin, to be the first
in path but not to conflict with existing jpackage-based packages.

%prep
%setup -q -n apache-ant-%{version}
( cd lib/optional && tar -xJf %{SOURCE1} )

%build
export JAVA_HOME=/opt/tuxjdk
bash ./build.sh -Ddist.dir=dist dist

%install
# removing windows scripts:
( cd dist/bin/ && rm -f *.bat *.cmd )
# we are building release build,
# so there should be only minimal debug info,
# and probably for a good reason:
export NO_BRP_STRIP_DEBUG='true'
# creating main dir:
install -dm 755 %{buildroot}/opt/%{name}
cp -R dist/* %{buildroot}/opt/%{name}/
install -Dm 755 %{SOURCE2} %{buildroot}/usr/local/bin/ant
# hardlinks instead of duplicates:
%fdupes %{buildroot}/opt/%{name}/

%files
%defattr(644,root,root,755)
/opt/%{name}
%attr(755,root,root) /opt/%{name}/bin/*

%files launchers
%defattr(755,root,root,755)
/usr/local/bin/*

%changelog
* Wed Jul  1 2015 baiduzhyi.devel@gmail.com
- Initial attempt to build ant for tuxjdk.
