#!/usr/bin/env bash
set -e

# This script requires the following environmentals:
# TRAVIS_MAVEN_SERVER_ID        - the id of the server that should be used f.e. appcom-maven-oss
# TRAVIS_MAVEN_USER             - the user that should be used to auth on the server f.e. appcom-ci
# TRAVIS_MAVEN_PWD              - the password / api_key of that user
# TRAVIS_MAVEN_ARTIFACT         - the artifact that should be downloaded 
#                                 (groupId:artifactId:version[:packaging][:classifier]) f.e. eu.appcom:djinni:470
# TRAVIS_MAVEN_URL              - the url of the repository f.e. https://api.bintray.com/content/appcom-interactive/appcom-maven-oss/djinni
# TRAVIS_MAVEN_FILE             - the file that should be downloaded (the destination where the file will be downloaded to)

declare DIR="$( dirname "${BASH_SOURCE[0]}" )"

mkdir ${HOME}/.m2 || true
cp ${DIR}/maven.settings.xml ${HOME}/.m2/settings.xml

mvn dependency:get -e \
      -Dartifact="${TRAVIS_MAVEN_ARTIFACT}" \
      -Dtransitive=false \
      -DremoteRepositories="${TRAVIS_MAVEN_SERVER_ID}::::${TRAVIS_MAVEN_URL}" \
      -Ddest="${TRAVIS_MAVEN_FILE}"
