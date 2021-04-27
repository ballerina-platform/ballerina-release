function getPackageVersionsofRepos () {
  local pagination="true"
  if [ -f "/tmp/package-versions.json" ]; then
    rm "/tmp/package-versions.json"
  fi
  if [ -f "/tmp/versions-to-delete.json" ]; then
    rm "/tmp/versions-to-delete.json"
  fi
  local monthago=$(date -d "$(date +%Y-%m-%d) -1 month" +%Y-%m-%d)
  curl -H "Authorization: bearer $GITHUB_TOKEN" -X POST -d '{"query":"query{repository(name:\"'$1'\",owner:\"ballerina-platform\"){packages(first:1,names:\"'$2'\"){nodes{versions(first:100,orderBy:{direction:ASC,field:CREATED_AT}){pageInfo{endCursor,hasNextPage},edges{node{statistics{downloadsTotalCount},id,version,files(first:1,orderBy:{direction:DESC,field:CREATED_AT}){nodes{updatedAt,name}}}}}}}}}"}' --url 'https://api.github.com/graphql' -o /tmp/package-versions.json
  local cursor=$(jq -r .data.repository.packages.nodes[].versions.pageInfo.endCursor /tmp/package-versions.json)
  local pagination=$(jq -r .data.repository.packages.nodes[].versions.pageInfo.hasNextPage /tmp/package-versions.json)
  jq -r '.data.repository.packages.nodes[].versions.edges[]|select ((.node.statistics.downloadsTotalCount==0) and (.node.files.nodes[0].updatedAt<="'$monthago'")).node.id' /tmp/package-versions.json >> /tmp/versions-to-delete.json
  while ("$pagination" != "false")
  do
    curl -H "Authorization: bearer $GITHUB_TOKEN" -X POST -d '{"query":"query{repository(name:\"'$1'\",owner:\"ballerina-platform\"){packages(first:1,names:\"'$2'\"){nodes{versions(first:100,orderBy:{direction:ASC,field:CREATED_AT},after:\"'$cursor'\"){pageInfo{endCursor,hasNextPage},edges{node{statistics{downloadsTotalCount},id,version,files(first:1,orderBy:{direction:DESC,field:CREATED_AT}){nodes{updatedAt,name}}}}}}}}}"}' --url 'https://api.github.com/graphql' -o /tmp/package-versions.json
    cursor=$(jq -r .data.repository.packages.nodes[].versions.pageInfo.endCursor /tmp/package-versions.json)
    pagination=$(jq -r .data.repository.packages.nodes[].versions.pageInfo.hasNextPage /tmp/package-versions.json)
    jq -r '.data.repository.packages.nodes[].versions.edges[]|select ((.node.statistics.downloadsTotalCount==0) and (.node.files.nodes[0].updatedAt<="'$monthago'")).node.id' /tmp/package-versions.json >> /tmp/versions-to-delete.json
  done
  cat /tmp/versions-to-delete.json | while read packageversionline
  do
    curl -X POST -H "Accept: application/vnd.github.package-deletes-preview+json" -H "Authorization: bearer $PACKAGE_DELETE_PAT" -d '{"query":"mutation { deletePackageVersion(input:{packageVersionId:\"'$packageversionline'\"}) { success }}"}' --url 'https://api.github.com/graphql'
  done
}

function getPackagesofRepos () {
  local cursor=""
  local pagination="true"
  if [ -f "/tmp/response.json" ]; then
    rm "/tmp/response.json"
  fi
  if [ -f "/tmp/packages.json" ]; then
    rm "/tmp/packages.json"
  fi
  while ("$pagination" != "false")
  do
    curl -H "Authorization: bearer $GITHUB_TOKEN" -X POST -d '{"query":"query{repository(name:\"'$1'\",owner:\"ballerina-platform\"){packages(first:100,orderBy:{field:CREATED_AT,direction:ASC}, after:\"'$cursor'\"){nodes{id,name},pageInfo{endCursor,hasNextPage}}}}"}' --url 'https://api.github.com/graphql' -o /tmp/response.json
    cursor=$(jq -r .data.repository.packages.pageInfo.endCursor /tmp/response.json)
    jq -r .data.repository.packages.nodes[].name /tmp/response.json >> /tmp/packages.json
    pagination=$(jq -r .data.repository.packages.pageInfo.hasNextPage /tmp/response.json)
  done

  cat /tmp/packages.json | while read packageline
  do
    getPackageVersionsofRepos "$1" "$packageline"
  done
}

if [ -f "/tmp/allversions.txt" ]; then
  rm "/tmp/allversions.txt"
fi
touch /tmp/allversions.txt

getPackagesofRepos "ballerina-lang"
cat /tmp/repos.json | while read repoline
do
  getPackagesofRepos "$repoline"
done
