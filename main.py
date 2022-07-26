import hashlib
import os
import shutil

import requests
from dotenv import load_dotenv
from intersight_auth import IntersightAuth, repair_pem
from tqdm import tqdm

load_dotenv()

intersight_base = os.environ.get('IntersightBaseUrl')

AUTH = IntersightAuth(
    api_key_id=os.environ.get('IntersightKeyId'),
    secret_key_string=repair_pem(os.environ.get('IntersightSecret'))
)

if not os.path.exists('Downloads'):
    os.makedirs('Downloads')


def get_intersight(url):
    RESPONSE = requests.request(
        method='GET',
        url=url,
        auth=AUTH,
    )
    return RESPONSE


def download_file(DownloadSpecs):
    filename = DownloadSpecs['Filename']
    if os.path.exists(f"Downloads/{filename}"):
        if hashlib.md5(open(f"Downloads/{filename}", 'rb').read()).hexdigest() == DownloadSpecs['Md5sum']:
            print(
                f"{filename}: already exists... MD5 matches ({DownloadSpecs['Md5sum']})")
        else:
            print(f"{filename}: already exists... MD5 FAIL... downloading")
            os.remove(f"Downloads/{filename}")
            download_file(DownloadSpecs)
    else:
        with requests.get(
            url=DownloadSpecs['Url'],
            stream=True
        ) as r:
            with tqdm.wrapattr(r.raw, "read", total=int(DownloadSpecs['Size']), desc=filename) as raw:
                with open(f"Downloads/{filename}", 'wb') as output:
                    shutil.copyfileobj(raw, output)
        if hashlib.md5(open(f"Downloads/{filename}", 'rb').read()).hexdigest() == DownloadSpecs['Md5sum']:
            print(
                f"{filename}: complete... MD5 matches ({DownloadSpecs['Md5sum']})")
        else:
            print(f"{filename}: MD5 FAIL... removing")
            os.remove(f"Downloads/{filename}")


# Appliance Bundle
appliance = get_intersight(
    f"{intersight_base}/software/ApplianceDistributables?$orderby=CreateTime%20desc&$top=1").json()['Results'][0]
download_file(get_intersight(
    f"{intersight_base}/softwarerepository/DownloadSpecs?$filter=File.Moid%20eq%20%27{appliance['Moid']}%27%20and%20ObjectType%20eq%20software.ApplianceDistributable").json())

# Hyperflex Bundle
hyperflex = get_intersight(
    f"{intersight_base}/software/HyperflexBundleDistributables?$orderby=CreateTime%20desc&$top=1").json()['Results'][0]
download_file(get_intersight(
    f"{intersight_base}/softwarerepository/DownloadSpecs?$filter=File.Moid%20eq%20%27{hyperflex['Moid']}%27%20and%20ObjectType%20eq%20software.HyperflexBundleDistributable").json())

# IKS Bundle
iks = get_intersight(
    f"{intersight_base}/software/IksBundleDistributables?$orderby=CreateTime%20desc&$top=1").json()['Results'][0]
download_file(get_intersight(
    f"{intersight_base}/softwarerepository/DownloadSpecs?$filter=File.Moid%20eq%20%27{iks['Moid']}%27%20and%20ObjectType%20eq%20software.IksBundleDistributable").json())

# Firmware
firmware = get_intersight(
    f"{intersight_base}/search/SearchItems?$filter=ObjectType%20eq%20%27firmware.Distributable%27%20and%20RecommendedBuild%20eq%20%27Y%27%20and%20Tags/any(t:t/Key%20eq%20%27cisco.meta.repositorytype%27%20and%20t/Value%20eq%20%27IntersightCloud%27)&$select=Moid,ObjectType&$inlinecount=allpages").json()['Results']
for spec in firmware:
    download_file(get_intersight(
        f"{intersight_base}/softwarerepository/DownloadSpecs?$filter=File.Moid%20eq%20%27{spec['Moid']}%27%20and%20ObjectType%20eq%20{spec['ObjectType']}").json())
