import jinja2
import shutil
import os
import yaml
import datetime

urls = []


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))

# Delete and recreate static folder
shutil.rmtree("./static", ignore_errors=True)
os.mkdir("./static")

# render about us page, create about-us folder
os.mkdir("./static/about-us")
template = template_env.get_template("about_us.html")
url = "https://magifind.com/about-us/"
with open("./static/about-us/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(canonical_url=url))
urls.append(url)

# render 404 page
template = template_env.get_template("404.html")
url = "https://magifind.com/404.html"
with open("./static/404.html", "w", encoding="utf-8") as f:
    f.write(template.render(canonical_url=url))

# render investors page, create investors folder
os.mkdir("./static/investors")
template = template_env.get_template("investors.html")
url = "https://magifind.com/investors/"
with open("./static/investors/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(canonical_url=url))
urls.append(url)
# render landing pages from landing_pages.yml
with open("./landing_pages.yml", "r") as f:
    landing_pages = yaml.safe_load(f)

for landing_page in landing_pages:
    slug = landing_page["slug"]
    os.mkdir("./static/" + slug)
    template = template_env.get_template("landing_page.html")
    url = "https://magifind.com/" + slug + "/"
    with open("./static/" + slug + "/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(landing_page=landing_page, canonical_url=url))
    urls.append(url)

# render ai_search_test.html
template = template_env.get_template("ai_search_test.html")
# create folder
os.mkdir("./static/ai-search-test")
url = "https://magifind.com/ai-search-test/"
with open("./static/ai-search-test/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(canonical_url=url))
urls.append(url)

# Blog
with open("./blog.yml", "r") as f:
    blog = yaml.safe_load(f)
os.mkdir("./static/blog")
for post in blog["posts"]:
    slug = post["slug"]
    os.mkdir("./static/blog/" + slug)
    post['image'] = post['image'].replace('.webp', '.svg')
    template = template_env.get_template("post.html")
    url = "https://magifind.com/blog/" + slug + "/"
    with open("./static/blog/" + slug + "/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(post=post, canonical_url=url))

    shutil.copyfile(
        "./images/" + post["image"], "./static/blog/" + slug + "/" + post["image"]
    )
template = template_env.get_template("blog.html")
url = "https://magifind.com/blog/"
with open("./static/blog/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(blog=blog, canonical_url=url))

# Home
with open("./faq.yml", "r") as f:
    faq = yaml.safe_load(f)
template = template_env.get_template("home.html")
url = "https://magifind.com/"
with open("./static/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(blog=blog, faq=faq, posts=blog["posts"], canonical_url=url))

# copy all files from ./images to ./static
shutil.copytree("./images", "./static/images")


# Sitemap
for post in blog["posts"]:
    urls.append("https://magifind.com/blog/" + post["slug"] + "/")
urls.append("https://magifind.com/blog/")
urls.append("https://magifind.com/")
sitemap = [
    {
        "loc": url,
        "lastmod": datetime.datetime.now().strftime("%Y-%m-%d"),
        "changefreq": "monthly",
    }
    for url in urls
]

# Render sitemap.xml and robots.txt
template = template_env.get_template("sitemap.xml")
with open("./static/sitemap.xml", "w") as f:
    f.write(template.render(sitemap=sitemap))
template = template_env.get_template("robots.txt")
with open("./static/robots.txt", "w") as f:
    f.write(template.render())

# copy dist folder
shutil.copytree("./css", "./static/css")
