from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    print(f"handle_starttag => tag is {tag}, attrs is {attrs}")

  def handle_data(self, data):
    print(f"handle_data => data is {data}")

  def handle_endtag(self, tag):
    print(f"handle_endtag => tag is {tag}")

parser = MyHTMLParser()
parser.feed('<title class="test">Python rocks!</title>')
