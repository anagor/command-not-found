Name:           command-not-found
Version:        1.3
Release:        12
Summary:        Command-not-found tool for ROSA and OpenMandriva
Group:          File tools
License:        GPLv2
URL:            https://abf.io/soft/command-not-found
Source0:        https://abf.io/soft/%{name}/archive/%{name}-%{version}.tar.gz
Patch0:		cnf-1.3-dnf.patch
Patch1:		command-not-found-fix-syntax-errors.patch
Patch2:       cnf-python3-and-sudo-fix.patch
BuildArch:      noarch

Requires:       command-not-found-data
Requires:       python-rpm
BuildRequires:  python(abi) >= 3.0
BuildRequires:	gettext

%description
When you call non-existent command in bash, you will get a 
list of packages (with repositories) where you can find this command
or similar ones.

%prep
%autosetup -p1
find . -name "*.py" |xargs 2to3 -w

%install
for d in $(python localizer.py --list); do\
    mkdir -p %{buildroot}%{_datadir}/locale/$d/LC_MESSAGES;\
    install -m 644 locale/$d/LC_MESSAGES/%{name}.mo %{buildroot}%{_datadir}/locale/$d/LC_MESSAGES/%{name}.mo;\
done
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp command-not-found.py  %{buildroot}%{_bindir}/cnf
cp handler.sh %{buildroot}%{_sysconfdir}/profile.d/91cnf.sh

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/cnf
%{_sysconfdir}/profile.d/91cnf.sh
