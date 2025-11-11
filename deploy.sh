#!/usr/bin/env sh

printf -- "Updating HTML\n"
python scripts/html_update.py
return_value=$?
if [ $return_value -ne 0 ]; then
  printf -- "HTML update had an effect! Confirm and re-run\n"
  return $return_value 2> /dev/null || exit $return_value
else

printf -- "Updating feed\n"
# This may update a timestamp and thus require an additional commit before
# deployment. We prefer not to make git commits programmatically.
python scripts/feed_update.py

if [ -n "$(git status -s)" ]; then
  printf -- "Git status is not clean. Commit changes and resolve untracked files.\n"
  return 1 2> /dev/null || exit 1
else
  gh_pages_branch="gh-pages"
  printf -- "Force pushing %s branch for GitHub pages\n" "$gh_pages_branch"
  # Deploy the site subtree, so the index is at the root as required
  # by Github pages.
  # Instead of "git subtree push", use a temporary local branch to make the force possible.
  gh_pages_temp_branch="$gh_pages_branch-temp"
  git subtree split --prefix site -b "$gh_pages_temp_branch"
  git push --force origin "$gh_pages_temp_branch:$gh_pages_branch"
  git branch -D "$gh_pages_temp_branch"
fi

fi  # HTML update check

# # Alternative to rsync files directly.
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
