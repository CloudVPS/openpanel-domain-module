# This file is part of OpenPanel - The Open Source Control Panel
# OpenPanel is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the Free 
# Software Foundation, using version 3 of the License.
#
# Please note that use of the OpenPanel trademark may be subject to additional 
# restrictions. For more information, please visit the Legal Information 
# section of the OpenPanel website on http://www.openpanel.com/

%define version 0.9.2

%define libpath /usr/lib
%ifarch x86_64
  %define libpath /usr/lib64
%endif

Summary: Domain node
Name: openpanel-mod-domain
Version: %version
Release: 1
License: GPLv3
Group: Development
Source: http://packages.openpanel.com/archive/openpanel-mod-domain-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-buildroot
Requires: openpanel-core >= 0.8.3
Requires: openpanel-mod-user

%description
Domain node
Openpanel domain node

%prep
%setup -q -n openpanel-mod-domain-%version

%build
BUILD_ROOT=$RPM_BUILD_ROOT

%install
BUILD_ROOT=$RPM_BUILD_ROOT
rm -rf ${BUILD_ROOT}
mkdir -p ${BUILD_ROOT}/var/opencore/modules/Domain.module
install -m 755 action ${BUILD_ROOT}/var/opencore/modules/Domain.module/action
cp module.xml *.html *.png ${BUILD_ROOT}/var/opencore/modules/Domain.module/
install -m 755 verify ${BUILD_ROOT}/var/opencore/modules/Domain.module/verify

%post
mkdir -p /var/opencore/conf/staging/Domain
chown opencore:authd /var/opencore/conf/staging/Domain

%files
%defattr(-,root,root)
/
