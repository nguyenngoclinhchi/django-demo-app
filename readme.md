# Django
- Link Document 4.2: https://docs.djangoproject.com/en/4.2/
- Check version Django: django-admin --version
- Create new project: django-admin startproject mysite
- Run server: python manage.py runserver
- Changing port: python manage.py runserver 6969
- Create new app: python manage.py startapp polls
- Create migrations to be applied into database: python manage.py makemigrations
- Create new, apply changes for database schema: python manage.py migrate
- Create new user: python manage.py createsuperuser

# Some documentations reference
- Link Editor Content: https://pypi.org/project/django-tinymce
- Render Markdown code: https://stackoverflow.com/questions/23031406/how-do-i-implement-markdown-in-django-1-6-app
- Upload path: https://www.geeksforgeeks.org/python-uploading-images-in-django
- Random name image: https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
- Delete image: https://stackoverflow.com/questions/2878490/how-to-delete-old-image-when-update-imagefield
- Feed parser: https://pypi.org/project/feedparser/
- Some lookup words to find:
1. **contains**: find value contains substring
2. **icontains**: find value contains substring - regardless uppercase/lowercase
3. **regex**: find value suitable for regex
4. **iregex**: find value suitable for regex - regardless uppercase/lowercase
   - re_path(r'^(?P<article_slug>[\w-]+)-a(?P<article_id>\d+)\.html$', views.article, name='article'),
   - re_path(r'^tin-tuc-tong-hop-(?P<feed_slug>[\w-]+)\.html$', views.feed, name='feed'),
   - re.search(r'^(?P<article_slug>[\w-]+)-a\d+\.html$', last_path)
- (...null=True, blank=True) (For cases allow field to be null or empty)
- (editable=False) (For cases not allowing admin to edit fields)

# Deloy Project: Đẩy website Django lên internet
- Server, VPS, Hosting, Domain...
  - Server, VPS, Hosting, and Domain are all related terms in the context of web infrastructure and online presence. Here's what each term generally refers to:

  1. **Server**: A server is a computer or a system that serves requests from other computers, known as clients. In the context of the internet, a server typically refers to a computer program or device that provides services or resources to other computers over a network. Servers can serve various purposes, such as hosting websites, applications, databases, or providing other network services like email, file storage, or media streaming.

  2. **VPS (Virtual Private Server)**: A VPS is a virtualized server environment created by partitioning a physical server into multiple virtual servers. Each virtual server operates independently and has its own operating system, resources (such as CPU, RAM, and disk space), and software applications. VPS hosting allows users to have more control and customization compared to shared hosting, as they have root access to their virtual server.

  3. **Hosting**: Hosting refers to the service of storing and serving website files, applications, or other digital content on a server connected to the internet. Web hosting providers offer various hosting solutions, including shared hosting, VPS hosting, dedicated hosting, and cloud hosting. The hosting service provides users with server space, resources, technical support, and infrastructure to make their websites or applications accessible online.

  4. **Domain**: A domain is a unique, human-readable address that represents a website on the internet. It consists of a name (such as "example") and a top-level domain (TLD) extension (such as ".com", ".org", ".net", etc.). Domains are used to identify and locate websites on the internet. When users type a domain name into a web browser's address bar, they are directed to the corresponding website hosted on a server. Domain names are registered through domain registrars, and they need to be renewed periodically to maintain ownership.