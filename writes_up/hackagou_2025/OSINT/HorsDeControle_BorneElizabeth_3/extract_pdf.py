import pymupdf as fitz, sys
d=fitz.open(sys.argv[1]); print(d.metadata)
for p in d:
    print("---page",p.number)
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines",[]):
            for s in l["spans"]:
                print(hex(s["color"]),round(s["size"],1),[round(x) for x in s["bbox"]],repr(s["text"]))
    print("images",p.get_images(), "links",p.get_links())
