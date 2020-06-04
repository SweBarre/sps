#!/bin/bash
if [[ ! "$(git branch --show-current)" == "master" ]];then
    echo "must be in master branch"
    exit 1
fi
if [[ ! -z "$(git status --short)" ]]; then
    echo "Master branch is not clean"
    exit 1
fi

current_version="$(sed -n 's/.*__version__ = "\(.*\)".*/\1/p'  src/sps/__init__.py)"
read -p "New version (current :$current_version): " new_version

git add -f "dist/sps-${current_version}-py36-none-any.whl"
git commit -m "Added wheel file for $current_version"
git tag -a "v${current_version}" -m "Version $current_version of sps"


sed -i 's/'"$current_version"'/'"$new_version"'/g' src/sps/__init__.py
updated_version="$(sed -n 's/.*__version__ = "\(.*\)".*/\1/p'  src/sps/__init__.py)"
git add src/sps/__init__.py
git commit -m "Created version $updated_version"
echo "Updated version to: $updated_version"
read -p "Do you want to push commits [y/N]: " response
if [[ "$response" == "y" ]];then
    git push
fi
read -p "Do you want to push tag [y/N]: " response
if [[ "$response" == "y" ]];then
    git push origin "v${current_version}"
fi
