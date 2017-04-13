%{?scl:%scl_package testng-remote}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

%global gittag testng-remote-parent-%{version}

Name:    %{?scl_prefix}testng-remote
Version: 1.1.0
Release: 1.%{baserelease}%{?dist}
Summary: Modules for running TestNG remotely
License: ASL 2.0
URL:     https://github.com/testng-team/testng-remote
Source0: https://github.com/testng-team/testng-remote/archive/%{gittag}.tar.gz

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.google.auto.service:auto-service)
BuildRequires:  %{?scl_prefix_java_common}mvn(com.google.code.gson:gson)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.testng:testng) >= 6.9.12

%description
TestNG Remote contains the modules for running TestNG remotely. This is
normally used by IDE to communicate with TestNG run-time, e.g. receive the
Test Result from run-time so that can display them on IDE views.

%package javadoc
Summary: API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n testng-remote-%{gittag}

# Avoid bundling gson
%pom_remove_plugin :maven-shade-plugin remote

# Plugin not in Fedora
%pom_remove_plugin :git-commit-id-plugin
%pom_remove_plugin :git-commit-id-plugin remote
sed -i -e 's/${git.branch}/%{gittag}/' -e 's/${git.commit.id}/%{gittag}/' -e 's/${git.build.version}/%{version}/' \
  remote/src/main/resources/revision.properties

%pom_remove_plugin -r :jacoco-maven-plugin

# Disable support for old versions of TestNG that are not in Fedora
%pom_disable_module remote6_9_7
%pom_disable_module remote6_5
%pom_disable_module remote6_0
%pom_remove_dep :testng-remote6_9_7 dist
%pom_remove_dep :testng-remote6_5 dist
%pom_remove_dep :testng-remote6_0 dist

# Package the shaded artifact (contains all testng-remote modules in a single jar)
%mvn_package ":testng-remote-dist:jar:shaded:"
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.1.0-1.2
- Remove unneeded jacoco plugin

* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.1.0-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Nov 01 2016 Mat Booth <mat.booth@redhat.com> - 1.1.0-1
- Update to tagged release
- Enable tests

* Mon Apr 25 2016 Mat Booth <mat.booth@redhat.com> - 1.0.0-0.2.gitfc5cfab
- Package the all-in-one shaded jar

* Mon Apr 25 2016 Mat Booth <mat.booth@redhat.com> - 1.0.0-0.1.gitfc5cfab
- Initial packaging of latest upstream snapshot.
