# python springerbook.py update
# python springerbook.py show all
# python springerbook.py show downloaded
# python springerbook.py show not-downloaded
# python springerbook.py download 10
# python springerbook.py download-E-ISBN xxx
import os
import time
import random
import requests
import click
from tqdm import tqdm
import pandas as pd
from lxml import etree

requests_session = requests.Session()

def download_url_and_save(url, filename=None, directory='.', headers=None, proxies=None):
    assert os.path.exists(directory)
    if filename is None:
        filename = os.path.join(directory, url.rsplit('/',1)[1])
    else:
        filename = os.path.join(directory, filename)
    response = requests_session.get(url, headers=headers, proxies=proxies, stream=True)
    response.raise_for_status()
    if not os.path.exists(filename):
        tmp_filename = filename + '.incomplete'
        tmp0 = {'total':int(response.headers['content-length']), 'unit':'iB', 'unit_scale':True}
        with open(tmp_filename, 'wb') as fid, tqdm(**tmp0) as progress_bar:
            for x in response.iter_content(chunk_size=1024): #1kiB
                progress_bar.update(len(x))
                fid.write(x)
        os.rename(tmp_filename, filename)
    return filename


CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)
DOWNLOAD_DIR = 'download'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# springer news see https://www.springernature.com/gp/librarians/landing/covid19-library-resources
XLSX_URL = 'https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v5'
XLSX_filename = 'Free+English+textbooks.xlsx'
XLSX_filepath = os.path.join(CACHE_DIR, XLSX_filename)
MY_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}



def EISBN_to_filename(EISBN):
    ret = 'E-ISBN-{}.pdf'.format(EISBN)
    return ret


def load_downloaded_item():
    ret = {x[7:-4] for x in os.listdir(DOWNLOAD_DIR) if x.startswith('E-ISBN-') and x.endswith('.pdf')}
    return ret


def download_item(OpenURL, EISBN):
    response = requests_session.get(OpenURL, headers=MY_HEADERS)
    response.raise_for_status()
    time.sleep(random.uniform(0.5,1.5)) #please be kind to springer server
    response.encoding='utf-8'
    html = etree.HTML(response.text)
    tmp0 = str(html.xpath('//div[@class="cta-button-container__item"]//a[contains(@href, ".pdf")]/@href')[0])
    full_url = 'https://link.springer.com' + tmp0
    download_url_and_save(full_url, EISBN_to_filename(EISBN), DOWNLOAD_DIR, headers=MY_HEADERS)
    time.sleep(random.uniform(0.5,1.5)) #please be kind to springer server


@click.group()
def click_entry():
    pass

@click.command(name='update', help='update ebook list')
def update_cache():
    download_url_and_save(XLSX_URL, XLSX_filename, CACHE_DIR, MY_HEADERS)

@click.command(name='show', help='one of {"all", "downloaded", "not-downloaded"}')
@click.argument('command')
def show_cache(command):
    pd0 = pd.read_excel(XLSX_filepath)
    tmp0 = load_downloaded_item()
    assert command in {'all', 'downloaded', 'not-downloaded'}
    if command == 'all':
        print(pd0)
    elif command=='downloaded':
        print(pd0[pd0['Electronic ISBN'].isin(tmp0)])
    else:
        tmp1 = set(pd0['Electronic ISBN'].values.tolist()) - tmp0
        print(pd0[pd0['Electronic ISBN'].isin(tmp1)])

@click.command(name='download', help='download first num_item ebook')
@click.argument('num_item')
def download_n_item(num_item):
    num_item = int(num_item)
    assert num_item>0
    pd0 = pd.read_excel(XLSX_filepath)
    tmp0 = load_downloaded_item()
    tmp1 = [x for x in pd0['Electronic ISBN'].values.tolist() if x not in tmp0][:num_item]
    pd1 = pd0[pd0['Electronic ISBN'].isin(tmp1)]
    for x0,x1 in zip(pd1['OpenURL'], pd1['Electronic ISBN']):
        print('[INFO] start downloading {}'.format(x1))
        download_item(x0, x1)

@click.command(name='download-E-ISBN', help='download one ebook by E-ISBN')
@click.argument('EISBN')
def download_E_ISBN(EISBN):
    tmp0 = load_downloaded_item()
    if EISBN in tmp0:
        print('EISBN="{}" already downloaded'.format(EISBN))
        return
    pd0 = pd.read_excel(XLSX_filepath)
    if EISBN not in set(pd0['Electronic ISBN'].values.tolist()):
        print('EISBN="{}" not in Open-access list'.format(EISBN))
        return
    tmp0 = pd0[pd0['Electronic ISBN']==EISBN].iloc[0]
    download_item(tmp0['OpenURL'], EISBN)


click_entry.add_command(update_cache)
click_entry.add_command(show_cache)
click_entry.add_command(download_n_item)
click_entry.add_command(download_E_ISBN)


if __name__=='__main__':
    if not os.path.exists(XLSX_filepath):
        download_url_and_save(XLSX_URL, XLSX_filename, CACHE_DIR, MY_HEADERS)
    click_entry()
