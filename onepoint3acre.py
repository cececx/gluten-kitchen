"""Gluten Kitchen.

Usage Example:
    $ python onepoint3acre.py <output-file> <filtered_page_url> <num_pages>
    
  output-file:         (string) The name for the output markdown file (will be stored at "output-file.md")
  filtered_page_url:   (string) Url to the first page after applying filter at 
                       https://www.1point3acres.com/bbs/forum-145-1.html. 
                       e.g. for google, use "https://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=145&sortid=311&searchoption[3088][value]=1&searchoption[3088][type]=radio&searchoption[3089][value][3]=3&searchoption[3089][type]=checkbox&searchoption[3090][value]=1&searchoption[3090][type]=radio&searchoption[3046][value]=1&searchoption[3046][type]=radio&searchoption[3109][value]=2&searchoption[3109][type]=radio&sortid=311&filter=sortid&orderby=dateline&page=1"
  num_pages:           (int) The number of pages you want to crawl. Usually 3 is optimal. 
    
Sample Output:
  processing G家onsite 面经
  processing 狗家上门
  processing [2018] Google onsite 面经
  processing 谷歌公司Youtube办公室面试经验
  processing 狗家onsite
  ...

"""

import requests
import sys
from bs4 import BeautifulSoup

# Cookies config.
COOKIES = {
    '4Oaf_61d6_auth': '',
    '4Oaf_61d6_saltkey': '',
}


# A kitchen that produces gluten ("面筋🌝") for travellers to pass through the
# evil interview valley.
class GlutenKitchen:

  def __init__(self, cookies_config):
    self._cookies = self.parse_coockies(cookies_config)

  def parse_coockies(self, cookies_json):
    jar = requests.cookies.RequestsCookieJar()
    for key, value in cookies_json.items():
      jar.set(key, value, domain='.1point3acres.com', path='/')
    return jar

  # Gets wild gluten.
  def produce_gluten(self, url):
    page = self.get_page(url)
    content = page.select('.t_fsz')[0].table.tr.td.get_text()
    return content

  # Gets glutens from a list page.
  def get_glutens(self, url):
    page = self.get_page(url)
    output = []
    gluten_list = page.select('#threadlisttableid')[0].find_all('tbody')[1:]
    for gluten in gluten_list:
      dom = gluten.select('.new')[0]
      title = dom.a.get_text()
      href = 'https://www.1point3acres.com/bbs/' + dom.a['href']
      description = dom.span.get_text().strip()
      content = self.produce_gluten(href)
      print('processing', title)
      self.output(title, href, description, content, output)
    return output

  def output(self, title, href, description, content, output):
    text = '### [{}]({})\n\n{}\n\n{}'.format(title, href, description, content)
    output.append(text)

  # Analyzes a sample page and saves raw html.
  def analyze(self, url):
    r = requests.get(url, cookies=self._cookies)
    res = r.text.replace('charset=gbk', 'charset=UTF-8')
    with open('res.html', 'w') as f:
      f.write(res)

  # Gets a pot of beautiful soup.
  def get_page(self, url):
    r = requests.get(url, cookies=self._cookies)
    return BeautifulSoup(r.text, 'html.parser')


if __name__ == '__main__':
  title = sys.argv[1]
  url_tmp = sys.argv[2]
  num_page = int(sys.argv[3])
  gluten_kitchen = GlutenKitchen(COOKIES)
  res = []
  for i in range(num_page):
    url = url_tmp.replace('page=1', 'page={}'.format(i + 1))
    res = res + gluten_kitchen.get_glutens(url)
  with open('{}.md'.format(title), 'w') as f:
    f.write('\n\n'.join(res))
