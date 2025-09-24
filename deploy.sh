#!/usr/bin/env sh

printf -- "Updating HTML\n"
python scripts/html_update.py
return_value=$?
if [ $return_value -ne 0 ]; then
  printf -- "HTML update had an effect! Confirm and re-run\n"
  exit $return_value
fi

printf -- "Updating feed\n"
python scripts/feed_update.py

printf -- "Pushing branch for GitHub pages\n"
# Deploy the site subtree, so the index is at the root as required
# by Github pages.
# There is no "force" option here.
# If this update is rejected, delete the gh-pages
# branch and reconfigure GitHub pages settings to publish
# it to patricksanan.org.
git subtree push --prefix site origin gh-pages

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
