import markdown

file = open("test.md", "r", encoding="utf-8").read()

h = markdown.markdown(file)

with open("h.html", "w", encoding="utf-8") as f:
    f.write(h)


