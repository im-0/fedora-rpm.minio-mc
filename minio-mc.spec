# TODO: Enable debuginfo (disabled for f35).
%global debug_package %{nil}

%global orig_version_date 2022-05-09
%global orig_version_time 04-08-26
%global orig_version %{orig_version_date}T%{lua: print(rpm.expand("%{orig_version_time}"):gsub("-", ":") .. "Z")}
%global orig_tag RELEASE.%{orig_version_date}T%{orig_version_time}Z

Name:       minio-mc
Version:    %{lua: print(rpm.expand("%{orig_version_date}"):gsub("-", ".") .. "." .. rpm.expand("%{orig_version_time}"):gsub("-", "."))}
Release:    1%{?dist}
Summary:    MinIO Client

License:    AGPLv3
URL:        https://github.com/minio/mc/
Source0:    https://github.com/minio/mc/archive/v%{orig_tag}/mc-%{orig_tag}.tar.gz

# $ GOPROXY=https://proxy.golang.org go mod vendor -v
# Contains mc-$TAG/vendor/*.
Source1:    mc-%{orig_tag}.go-mod-vendor.tar.xz

Source2:    minio-mc.bash-completion

BuildRequires:  golang >= 1.17


%description
MinIO Client (mc) provides a modern alternative to UNIX commands like
ls, cat, cp, mirror, diff, find etc. It supports filesystems and Amazon
S3 compatible cloud storage service (AWS Signature v2 and v4).


%prep
%autosetup -p1 -b0 -n mc-%{orig_tag}
%autosetup -p1 -b1 -n mc-%{orig_tag}

sed -i 's,^\([[:space:]]*Version[[:space:]]*=[[:space:]]*\)".*$,\1"%{orig_version}",' cmd/build-constants.go
sed -i 's,^\([[:space:]]*ReleaseTag[[:space:]]*=[[:space:]]*\)".*$,\1"%{orig_tag}",' cmd/build-constants.go


%build
export GO111MODULE="on"
export CGO_ENABLED=0
go build -v \
        -ldflags "-B 0x$(head -c20 /dev/urandom | od -An -tx1 | tr -d ' \n')"


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/bash-completion/completions

mv mc %{buildroot}/%{_bindir}/%{name}
cp %{SOURCE2} %{buildroot}/%{_datadir}/bash-completion/completions/%{name}


%files
/%{_bindir}/%{name}
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}


%changelog
* Thu May 12 2022 Ivan Mironov <mironov.ivan@gmail.com> - 2022.05.09.04.08.26-1
- Update to RELEASE.2022-05-09T04-08-26Z

* Tue Sep 21 2021 Ivan Mironov <mironov.ivan@gmail.com> - 2021.09.02.09.21.27-1
- Update to RELEASE.2021-09-02T09-21-27Z

* Sat Jun 12 2021 Ivan Mironov <mironov.ivan@gmail.com> - 2021.06.08.01.29.37-1
- Initial packaging
