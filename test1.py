from bs4 import BeautifulSoup

text = '''
<td><a href="http://www.fakewebsite.com">Please can you strip me?</a>
<br/><a href="http://www.fakewebsite.com">I am waiting....</a>
</td>
'''
soup = BeautifulSoup(text)

print(soup.get_text())
