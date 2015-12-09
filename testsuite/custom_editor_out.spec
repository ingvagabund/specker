%install
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 ${RPM_BUILD_ROOT}%{_bindir}
install -m 755 -p tcsh ${RPM_BUILD_ROOT}%{_bindir}/tcsh
install -m 777 -p \
tcsh.man ${RPM_BUILD_ROOT}%{_mandir}/man1/tcsh.1
ln -sf tcsh ${RPM_BUILD_ROOT}%{_bindir}/csh
ln -sf tcsh.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/csh.1

