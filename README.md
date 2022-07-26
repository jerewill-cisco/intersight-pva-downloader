# Automate downloading from Intersight.com to update PVA

The most recently published file for the Appliamce bundle, Hyperflex bundle, and IKS bundle is downloaded.  All of the currently 'Recommended' firmware bundles are downloaded. 

MD5s are checked for existing files and after download.  Files that don't match are deleted.  Files that already exist and match MD5 are not downloaded again.

TQDM is used to provide progress on downloads.
