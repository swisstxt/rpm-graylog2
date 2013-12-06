HOME=$(shell pwd)
VERSION="0.12.0"
RELEASE="1"

all: build

clean:
	rm -rf ./rpmbuild
	mkdir -p ./rpmbuild/SPECS/ ./rpmbuild/SOURCES/

download-upstream:
	./download graylog2-server-${VERSION}.tar.gz https://github.com/Graylog2/graylog2-server/releases/download/${VERSION}/graylog2-server-${VERSION}.tar.gz
	./download graylog2-web-interface-${VERSION}.tar.gz https://github.com/Graylog2/graylog2-web-interface/archive/${VERSION}.tar.gz

build: clean download-upstream
	cp -r ./SPECS/* ./rpmbuild/SPECS/
	cp -r ./SOURCES/* ./rpmbuild/SOURCES/
	rpmbuild -ba SPECS/graylog2-server.spec \
		--define "ver ${VERSION}" \
		--define "rel ${RELEASE}" \
		--define "_topdir %(pwd)/rpmbuild" \
		--define "_builddir %{_topdir}" \
		--define "_rpmdir %{_topdir}" \
		--define "_srcrpmdir %{_topdir}"
	rpmbuild -ba SPECS/graylog2-web-interface.spec \
		--define "ver ${VERSION}" \
		--define "rel ${RELEASE}" \
		--define "_topdir %(pwd)/rpmbuild" \
		--define "_builddir %{_topdir}" \
		--define "_rpmdir %{_topdir}" \
		--define "_srcrpmdir %{_topdir}"
