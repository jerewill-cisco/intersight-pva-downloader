# Automate downloading from Intersight.com to update PVA

This is the kind of thing you could set up as a recurring cron job.  It uses API keys to access Intersight.  See [example.env](example.env).

The most recently published file for the Appliance bundle, Hyperflex bundle, and IKS bundle is downloaded.  All of the currently 'Recommended' firmware bundles are downloaded.

MD5s are checked to validate existing files and for new files after download.  Files that would be downloaded but fail to validate against known MD5 hashes are deleted and redownloaded.  Files that already exist and match MD5 are not downloaded again.  No files are removed automatically, so some other mechanism will have to be employed if storage utilization becomes a problem.

[TQDM](https://github.com/tqdm/tqdm) is used to provide progress on downloads.

[Intersight-auth](https://github.com/cgascoig/intersight-auth) is used to authenticate to Intersight using the Python [Requests](https://requests.readthedocs.io) module.
