Provides: golang(%{import_path}/backend) = %{version}-%{release}
Provides: golang(%{import_path}/backend/alloc) = %{version}-%{release}

%package devel
Provides: golang(%{import_path}/backend) = %{version}-%{release}
Provides: golang(%{import_path}/backend/alloc) = %{version}-%{release}
Provides: golang(%{import_path}/backend/awsvpc) = %{version}-%{release}
Provides: golang(%{import_path}/backend/gce) = %{version}-%{release}
Provides: golang(%{import_path}/backend/hostgw) = %{version}-%{release}
Provides: golang(%{import_path}/backend/udp) = %{version}-%{release}
Provides: golang(%{import_path}/backend/vxlan) = %{version}-%{release}
Provides: golang(%{import_path}/network) = %{version}-%{release}
Provides: golang(%{import_path}/pkg/ip) = %{version}-%{release}
Provides: golang(%{import_path}/remote) = %{version}-%{release}
Provides: golang(%{import_path}/subnet) = %{version}-%{release}
