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
with open("./static/about-us/index.html", "w", encoding="utf-8") as f:
    f.write(template.render())
urls.append("https://magifind.com/about-us/")

os.mkdir("./static/investors")
template = template_env.get_template("investors.html")
with open("./static/investors/index.html", "w", encoding="utf-8") as f:
    f.write(template.render())
urls.append("https://magifind.com/investors/")

# render landing pages from landing_pages.yml
with open("./landing_pages.yml", "r") as f:
    landing_pages = yaml.safe_load(f)

for landing_page in landing_pages:
    slug = landing_page["slug"]
    os.mkdir("./static/" + slug)
    template = template_env.get_template("landing_page.html")
    with open("./static/" + slug + "/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(landing_page=landing_page))
    urls.append("https://magifind.com/" + slug + "/")

# render ai_search_test.html
template = template_env.get_template("ai_search_test.html")
# create folder
os.mkdir("./static/ai-search-test")
with open("./static/ai-search-test/index.html", "w", encoding="utf-8") as f:
    f.write(template.render())
urls.append("https://magifind.com/ai-search-test/")

# Blog
with open("./blog.yml", "r") as f:
    blog = yaml.safe_load(f)
os.mkdir("./static/blog")
for post in blog["posts"]:
    slug = post["slug"]
    os.mkdir("./static/blog/" + slug)
    template = template_env.get_template("post.html")
    with open("./static/blog/" + slug + "/index.html", "w", encoding="utf-8") as f:
        f.write(template.render(post=post))

    shutil.copyfile(
        "./images/" + post["image"], "./static/blog/" + slug + "/" + post["image"]
    )
template = template_env.get_template("blog.html")
with open("./static/blog/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(blog=blog))

# Home
with open("./faq.yml", "r") as f:
    faq = yaml.safe_load(f)
template = template_env.get_template("home.html")
with open("./static/index.html", "w", encoding="utf-8") as f:
    f.write(template.render(blog=blog, faq=faq, posts=blog["posts"]))

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
