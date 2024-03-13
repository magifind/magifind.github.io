import jinja2
import shutil
import os
import yaml
import datetime

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))

# Delete and recreate static folder
shutil.rmtree("./static", ignore_errors=True)
os.mkdir("./static")

# render about us page, create about-us folder
os.mkdir("./static/about-us")
template = template_env.get_template("about_us.html")
with open("./static/about-us/index.html", "w", encoding="utf-8") as f:
    f.write(template.render())


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
    f.write(template.render(blog=blog, faq=faq))

# copy all files from ./images to ./static
shutil.copytree("./images", "./static/images")


# Sitemap
urls = []
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
shutil.copytree("./dist", "./static/dist")
