#!/usr/bin/env python
# encoding: utf-8
from lxml import html
import requests
import npyscreen
import re
import textwrap
from itertools import chain
class PyBashApp(npyscreen.NPSApp):
    def load_citations(self,url):
        page = requests.get(url)
        tree = html.fromstring(re.sub("(<br>)|(<br />|(\r)|(\n))", "\r\n", page.content.decode('windows-1251')))
        cites = tree.xpath('//div[@class="text"]/text()')
        texts = []
        for c in cites:
            texts.append(str(c))

        all_text = ""
        for t in texts:
            t = textwrap.wrap(t, 100, replace_whitespace=False)
            t = "\n".join(t)
            # all_text+="Следующая:\n"+t+"\n\n"
            all_text += "_" * 100 + "\n\n" + t + "\n\n"
            # widg.append(F.add_widget(npyscreen.TitleMultiLine,name = 'Цитата',values=t.split('\n'),scroll_end=True))

        # texts[0]="Следующая:\n"+texts[0]
        #texts[0] = "_" * 100 + "\n\n" + texts[0]
        return all_text

    def display_citations(self,citations):
        self.cite_id.values=citations
        self.cite_id.display()
        self.Form.refresh()

    def load_random(self):
        self.display_citations(self.load_citations('http://bash.im/random').split("\n"))

    def load_abyss(self):
        self.display_citations(self.load_citations('http://bash.im/abyss').split("\n"))
    def load_new(self):
        self.display_citations(self.load_citations('http://bash.im/').split("\n"))
    def load_best(self):
        self.display_citations(self.load_citations('http://bash.im/best').split("\n"))

    def main(self):
        self.Form  = npyscreen.FormWithMenus(name = "PyBashImGetter",)
        self.cite_id=self.Form.add_widget(npyscreen.TitleMultiLine, name='Citations',values="")
        self.load_new()
        menu=self.Form.new_menu()
        menu.addItem("Load from front page", self.load_new)
        menu.addItem("Load best", self.load_best)
        menu.addItem("Load abyss",self.load_abyss)
        menu.addItem("Load new random citations", self.load_random)
        menu.addItem("Exit", lambda:exit())
        #F.add_handlers(hndlrs)
        self.Form.edit()

if __name__ == "__main__":

    App = PyBashApp()
    App.run()