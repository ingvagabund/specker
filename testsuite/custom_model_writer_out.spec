Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.23
Release: 11%{?dist}
License: GPLv3+
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source101:  coreutils-DIR_COLORS
Source106:  coreutils-colorls.csh

Provides: /bin/basename
Provides: /bin/cat
Provides: /bin/chgrp
Provides: /bin/chmod
Provides: /bin/chown
Provides: /bin/cut

Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
Requires(post): grep

%post
%{_bindir}/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
  %{_infodir}/dir.rpmmodify || exit 0
    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%doc ABOUT-NLS NEWS README THANKS TODO
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/basename
%{_bindir}/cat
%{_bindir}/chgrp
%{_bindir}/chmod
%{_bindir}/chown
%{_bindir}/cut

