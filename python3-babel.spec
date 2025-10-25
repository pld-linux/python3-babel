#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	babel
%define		pypi_name	babel
Summary:	Babel - internationalization library for Python 2
Summary(pl.UTF-8):	Babel - biblioteka umiędzynaradawiająca dla Pythona 2
Name:		python3-%{module}
Version:	2.17.0
Release:	5
License:	BSD-like
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/babel/
Source0:	https://pypi.debian.net/babel/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	726d2ed119255a011d248ac0c9caa24a
URL:		http://babel.pocoo.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-devel-tools >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
BuildRequires:	python3-pytz >= 2015.7
%if %{with tests}
BuildRequires:	python3-freezegun
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
%endif
%{?with_doc:BuildRequires:	sphinx-pdg}
Requires:	python3-modules
Obsoletes:	python-Babel < 0.9.5-2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Babel is a Python library that provides an integrated collection of
utilities that assist with internationalizing and localizing Python
applications (in particular web-based applications).

%description -l pl.UTF-8
Babel to biblioteka Pythona zawierająca zintegrowany zbiór narzędzi
pomagających przy umiędzynaradawianiu i lokalizowaniu aplikacji w
Pythonie (w szczególności aplikacji WWW).

%package apidocs
Summary:	Python Babel API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona Babel
Group:		Documentation

%description apidocs
Python Babel API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona Babel.

%prep
%setup -q -n babel-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
TZ=UTC \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs -j1 html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{pybabel,pybabel3}

find $RPM_BUILD_ROOT%{py3_sitescriptdir}/babel/locale-data -name '*.dat' | \
	sed -e "s#^$RPM_BUILD_ROOT##" | \
	sed -ne 's,.*/\([a-z][a-z][a-z]\?\)\(_[0-9][0-9][0-9]\|_[A-Z][a-z][a-z][a-z]\)\?\(_[A-Z][A-Z]\)\?\(_POSIX\)\?\.dat,&,p' > py3.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files -f py3.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.rst LICENSE
%attr(755,root,root) %{_bindir}/pybabel3
%dir %{py3_sitescriptdir}/babel
%{py3_sitescriptdir}/babel/__pycache__
%{py3_sitescriptdir}/babel/global.dat
%{py3_sitescriptdir}/babel/*.py
%{py3_sitescriptdir}/babel/localtime
%{py3_sitescriptdir}/babel/py.typed
%dir %{py3_sitescriptdir}/babel/locale-data
%{py3_sitescriptdir}/babel/locale-data/root.dat
%lang(be_BY@tarask) %{py3_sitescriptdir}/babel/locale-data/be_TARASK.dat
%lang(ca_ES@valencia) %{py3_sitescriptdir}/babel/locale-data/ca_ES_VALENCIA.dat
%lang(el) %{py3_sitescriptdir}/babel/locale-data/el_POLYTON.dat
%{py3_sitescriptdir}/babel/messages
%{py3_sitescriptdir}/babel-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
