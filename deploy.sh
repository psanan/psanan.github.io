#!/usr/bin/env sh

if [ -n "$(git status -s)" ]; then
  printf -- "Git status is not clean. Commit changes and resolve untracked files.\n"
  return 1
else

printf -- "Updating HTML\n"
python scripts/html_update.py
return_value=$?
if [ $return_value -ne 0 ]; then
  printf -- "HTML update had an effect! Confirm and re-run\n"
  return $return_value
else

printf -- "Updating feed\n"
python scripts/feed_update.py

gh_pages_branch="gh-pages"
printf -- "Pushing $gh_pages_branch for GitHub pages\n"
# Deploy the site subtree, so the index is at the root as required
# by Github pages.
# Instead of "git subtree push", use a temporary local branch to make the force possible.

git subtree split --prefix site -b gh-pages-temp
git push --force origin gh-pages-temp:$gh_pages_branch
git branch -D gh-pages-temp

fi  # HTML update check
fi  # git status check

# # Alternate to rsync files directly.
# # This relies on an SSH alias "webhost"
# # to define where to upload files.
# # See e.g. https://wiki.debian.org/SshAliases
#
# target_dir="public_html"
#
# printf -- "Updating non-image files\n"
# # Images are big so don't update existing files in any "image" directories
# # If you want to wipe out some images to update, do it manually for now, like
# # ssh webhost  "rm -rf public_html/images/foo/"
# rsync -r --progress --delete --exclude=images/ site/ "webhost:$target_dir/"
#
# printf -- "Uploading new image files\n"
# rsync -r --progress --delete --ignore-existing site/images/ "webhost:$target_dir/images/"
