#!/usr/bin/env bash
set -e

# This script requires the following environmentals:
# TRAVIS_MAVEN_SERVER_ID     - the id of the server that should be used f.e. appcom-maven-oss
# TRAVIS_MAVEN_USER          - the user that should be used to auth on the server f.e. appcom-ci
# TRAVIS_MAVEN_PWD           - the password / api_key of that user
# TRAVIS_MAVEN_GROUP_ID      - the maven group id f.e. eu.appcom
# TRAVIS_MAVEN_ARTIFACT_ID   - the artifact id f.e. djinni
# TRAVIS_MAVEN_VERSION       - the version of the artifact
# TRAVIS_MAVEN_URL           - the url of the repository f.e. https://api.bintray.com/content/appcom-interactive/appcom-maven-oss/djinni
# TRAVIS_MAVEN_FILE          - the file that should be uploaded

declare DIR="$( dirname "${BASH_SOURCE[0]}" )"

mkdir ${HOME}/.m2 || true
cp ${DIR}/maven.settings.xml ${HOME}/.m2/settings.xml

mvn deploy:deploy-file -e \
      -DgroupId="${TRAVIS_MAVEN_GROUP_ID}" \
      -DartifactId="${TRAVIS_MAVEN_ARTIFACT_ID}" \
      -Dversion="${TRAVIS_MAVEN_VERSION}" \
      -DgeneratePom=true \
      -DrepositoryId="${TRAVIS_MAVEN_SERVER_ID}" \
      -Durl="${TRAVIS_MAVEN_URL}" \
      -Dfile="${TRAVIS_MAVEN_FILE}"
