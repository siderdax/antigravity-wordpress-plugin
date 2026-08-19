#!/usr/bin/env python3
"""
WordPress.com REST API CLI Utility for Antigravity & Hermes
Author: kyi
"""

import os
import sys
import argparse
import json
import urllib.parse
import urllib.request
import ssl
try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except Exception:
    SSL_CONTEXT = ssl.create_default_context()

def load_env():
    """
    Search and load environment variables from distinct Antigravity, Antigravity CLI, 
    Workspace, and Hermes configuration paths:
    1. Local workspace .env (./.env)
    2. Plugin folder .env (~/Projects/antigravity-wordpress-plugin/.env)
    3. Antigravity CLI specific path (~/.antigravitycli/.env)
    4. Gemini Antigravity CLI path (~/.gemini/antigravity-cli/.env)
    5. Gemini Antigravity IDE path (~/.gemini/antigravity/.env)
    6. Shared config path (~/.gemini/config/.env or ~/.gemini/.env)
    7. Antigravity Server path (~/.antigravity-server/.env)
    8. Hermes env (~/.hermes/.env)
    """
    env_paths = [
        os.path.abspath('.env'),
        os.path.expanduser('~/Projects/antigravity-wordpress-plugin/.env'),
        os.path.expanduser('~/.antigravitycli/.env'),
        os.path.expanduser('~/.gemini/antigravity-cli/.env'),
        os.path.expanduser('~/.gemini/antigravity/.env'),
        os.path.expanduser('~/.gemini/config/.env'),
        os.path.expanduser('~/.gemini/.env'),
        os.path.expanduser('~/.antigravity-server/.env'),
        os.path.expanduser('~/.hermes/.env')
    ]

    env_vars = {}
    for path in env_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        key = k.strip()
                        val = v.strip().strip('"').strip("'")
                        if key not in env_vars:
                            env_vars[key] = val
    return env_vars

env = load_env()
SITE_ID = os.environ.get('WORDPRESS_SITE_ID') or env.get('WORDPRESS_SITE_ID', '165329412')
ACCESS_TOKEN = os.environ.get('WORDPRESS_ACCESS_TOKEN') or env.get('WORDPRESS_ACCESS_TOKEN')
BASE_URL = f'https://public-api.wordpress.com/rest/v1.1/sites/{SITE_ID}'

def api_request(endpoint, method='GET', data=None, params=None):
    if not ACCESS_TOKEN:
        print("Error: WORDPRESS_ACCESS_TOKEN is not set in environment or any .env files.")
        print("Checked paths: ./.env, ~/.antigravitycli/.env, ~/.gemini/antigravity-cli/.env, ~/.gemini/config/.env, ~/.hermes/.env")
        sys.exit(1)

    url = f"{BASE_URL}{endpoint}"
    if params:
        query_string = urllib.parse.urlencode(params)
        url += f"?{query_string}"

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'User-Agent': 'Antigravity-WP-Plugin/1.0'
    }

    body = None
    if data is not None:
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
        body = urllib.parse.urlencode(data).encode('utf-8')

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {err_msg}")
        sys.exit(1)
    except Exception as e:
        print(f"Request Error: {e}")
        sys.exit(1)

# === Commands ===

def cmd_posts_list(args):
    params = {'number': args.number}
    if args.status:
        params['status'] = args.status
    res = api_request('/posts', params=params)
    posts = res.get('posts', [])
    print(f"Total Posts: {res.get('found', len(posts))}")
    print("-" * 80)
    for p in posts:
        tags = list(p.get('tags', {}).keys()) if isinstance(p.get('tags'), dict) else []
        cats = list(p.get('categories', {}).keys()) if isinstance(p.get('categories'), dict) else []
        print(f"[{p['ID']}] {p['title']}")
        print(f"    Status: {p['status']} | Date: {p['date']}")
        print(f"    Cats: {cats} | Tags: {tags}")
        print(f"    URL: {p['URL']}\n")

def cmd_posts_get(args):
    p = api_request(f"/posts/{args.post_id}")
    tags = list(p.get('tags', {}).keys()) if isinstance(p.get('tags'), dict) else []
    cats = list(p.get('categories', {}).keys()) if isinstance(p.get('categories'), dict) else []
    print(f"ID: {p['ID']}")
    print(f"Title: {p['title']}")
    print(f"Status: {p['status']}")
    print(f"Date: {p['date']}")
    print(f"Categories: {cats}")
    print(f"Tags: {tags}")
    print(f"URL: {p['URL']}")
    print("-" * 60)
    print("Content:")
    print(p.get('content', ''))

def cmd_posts_create(args):
    content = ""
    if getattr(args, 'content_file', None) and os.path.exists(args.content_file):
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    elif args.content:
        content = args.content
    data = {
        'title': args.title,
        'content': content,
        'status': args.status
    }
    if args.tags:
        data['tags'] = args.tags
    if args.categories:
        data['categories'] = args.categories

    p = api_request('/posts/new', method='POST', data=data)
    print(f"Successfully Created Post! ID: {p['ID']}")
    print(f"Title: {p['title']}")
    print(f"Status: {p['status']}")
    print(f"URL: {p['URL']}")

def cmd_posts_update(args):
    data = {}
    if args.title: data['title'] = args.title
    if getattr(args, 'content_file', None) and os.path.exists(args.content_file):
        with open(args.content_file, 'r', encoding='utf-8') as f:
            data['content'] = f.read()
    elif args.content: data['content'] = args.content
    if args.status: data['status'] = args.status
    if args.tags is not None: data['tags'] = args.tags
    if args.categories is not None: data['categories'] = args.categories

    p = api_request(f"/posts/{args.post_id}", method='POST', data=data)
    print(f"Successfully Updated Post {p['ID']}!")
    print(f"Title: {p['title']}")
    print(f"Status: {p['status']}")

def cmd_posts_delete(args):
    res = api_request(f"/posts/{args.post_id}/delete", method='POST')
    print(f"Deleted Post {args.post_id}: {res}")

def cmd_tags_list(args):
    res = api_request('/tags', params={'number': 100})
    tags = res.get('tags', [])
    print(f"Total Tags: {len(tags)}")
    print("-" * 60)
    for t in sorted(tags, key=lambda x: x['name']):
        print(f"Name: {t['name']:20s} | Slug: {t['slug']:20s} | Posts: {t['post_count']}")

def cmd_tags_cleanup(args):
    res = api_request('/tags', params={'number': 200})
    tags = res.get('tags', [])
    unused = [t for t in tags if t['post_count'] == 0]
    print(f"Found {len(unused)} unused tags to cleanup.")
    for t in unused:
        slug = t['slug']
        del_res = api_request(f"/tags/slug:{slug}/delete", method='POST')
        print(f"Deleted unused tag '{t['name']}': {del_res.get('success', 'done')}")

def cmd_categories_list(args):
    res = api_request('/categories', params={'number': 100})
    cats = res.get('categories', [])
    print(f"Total Categories: {len(cats)}")
    print("-" * 60)
    for c in sorted(cats, key=lambda x: x['name']):
        print(f"Name: {c['name']:25s} | Slug: {c['slug']:20s} | Posts: {c['post_count']}")

def cmd_themes_get(args):
    t = api_request('/themes/mine')
    print(f"Current Active Theme:")
    print(f"  ID: {t.get('id')}")
    print(f"  Name: {t.get('name')}")
    print(f"  Version: {t.get('version')}")
    print(f"  Author: {t.get('author')}")

def cmd_themes_list(args):
    res = api_request('/themes', params={'number': 30})
    themes = res.get('themes', [])
    print(f"Total Themes Found: {len(themes)}")
    print("-" * 60)
    if isinstance(themes, dict):
        for k, v in list(themes.items())[:20]:
            name = v.get('name') if isinstance(v, dict) else v
            print(f"ID: {k:30s} | Name: {name}")
    elif isinstance(themes, list):
        for t in themes[:20]:
            if isinstance(t, dict):
                print(f"ID: {t.get('id', ''):30s} | Name: {t.get('name')}")
            else:
                print(f"Theme Slug: {t}")

def cmd_themes_set(args):
    data = {'theme': args.theme}
    t = api_request('/themes/mine', method='POST', data=data)
    print(f"Successfully activated theme '{args.theme}'!")
    print(f"  Active Theme Name: {t.get('name')}")
    print(f"  Theme ID: {t.get('id')}")

def cmd_token(args):
    client_id = os.environ.get('WORDPRESS_CLIENT_ID') or env.get('WORDPRESS_CLIENT_ID')
    client_secret = os.environ.get('WORDPRESS_CLIENT_SECRET') or env.get('WORDPRESS_CLIENT_SECRET')
    redirect_uri = os.environ.get('WORDPRESS_REDIRECT_URI') or env.get('WORDPRESS_REDIRECT_URI', 'https://steelcup.home.blog/')
    
    if not client_id or not client_secret:
        print("Error: WORDPRESS_CLIENT_ID or WORDPRESS_CLIENT_SECRET is missing.")
        sys.exit(1)
        
    url = "https://public-api.wordpress.com/oauth2/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code': args.code
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'User-Agent': 'Antigravity-WP-Plugin/1.0'
    }
    body = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT) as response:
            res_body = response.read().decode('utf-8')
            data = json.loads(res_body)
            new_token = data.get('access_token')
            if not new_token:
                print(f"Error: No access_token returned: {data}")
                sys.exit(1)
            print(f"Successfully obtained new access token!")
            print(f"Site ID / Blog ID: {data.get('blog_id')}")
            print(f"Blog URL: {data.get('blog_url')}")
            
            # Update .env files
            env_paths = [
                os.path.expanduser('~/.hermes/.env'),
                os.path.expanduser('~/.gemini/config/.env'),
                os.path.expanduser('~/.gemini/antigravity-cli/.env'),
                os.path.abspath('.env')
            ]
            updated_any = False
            for p in env_paths:
                if os.path.exists(p):
                    with open(p, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    token_found = False
                    new_lines = []
                    for line in lines:
                        if line.startswith('WORDPRESS_ACCESS_TOKEN='):
                            new_lines.append(f'WORDPRESS_ACCESS_TOKEN="{new_token}"\n')
                            token_found = True
                        else:
                            new_lines.append(line)
                    if not token_found:
                        new_lines.append(f'WORDPRESS_ACCESS_TOKEN="{new_token}"\n')
                    with open(p, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Updated token in: {p}")
                    updated_any = True
            if not updated_any:
                hermes_env = os.path.expanduser('~/.hermes/.env')
                with open(hermes_env, 'a', encoding='utf-8') as f:
                    f.write(f'\nWORDPRESS_ACCESS_TOKEN="{new_token}"\n')
                print(f"Saved token to: {hermes_env}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error {e.code}: {err_msg}")
        sys.exit(1)
    except Exception as e:
        print(f"Request Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="WordPress.com REST API CLI for Antigravity")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Token
    p_token = subparsers.add_parser('token', help='Exchange authorization code for access token')
    p_token.add_argument('--code', required=True, help='Authorization code from OAuth redirect')
    p_token.set_defaults(func=cmd_token)

    # Posts
    p_posts = subparsers.add_parser('posts', help='Manage posts')
    p_posts_sub = p_posts.add_subparsers(dest='subcommand')

    p_list = p_posts_sub.add_parser('list', help='List recent posts')
    p_list.add_argument('-n', '--number', type=int, default=10, help='Number of posts')
    p_list.add_argument('-s', '--status', type=str, help='Filter status (publish, draft)')
    p_list.set_defaults(func=cmd_posts_list)

    p_get = p_posts_sub.add_parser('get', help='Get post detail')
    p_get.add_argument('post_id', type=int, help='Post ID')
    p_get.set_defaults(func=cmd_posts_get)

    p_create = p_posts_sub.add_parser('create', help='Create new post')
    p_create.add_argument('--title', required=True, help='Post title')
    p_create.add_argument('--content', help='Post content (HTML or Text)')
    p_create.add_argument('--content-file', help='Path to content file (HTML or Text)')
    p_create.add_argument('--status', default='publish', choices=['publish', 'draft', 'private'], help='Post status')
    p_create.add_argument('--tags', help='Comma separated tags')
    p_create.add_argument('--categories', help='Comma separated categories')
    p_create.set_defaults(func=cmd_posts_create)

    p_update = p_posts_sub.add_parser('update', help='Update existing post')
    p_update.add_argument('post_id', type=int, help='Post ID')
    p_update.add_argument('--title', help='Post title')
    p_update.add_argument('--content', help='Post content')
    p_update.add_argument('--content-file', help='Path to content file (HTML or Text)')
    p_update.add_argument('--status', choices=['publish', 'draft', 'private'], help='Post status')
    p_update.add_argument('--tags', help='Comma separated tags')
    p_update.add_argument('--categories', help='Comma separated categories')
    p_update.set_defaults(func=cmd_posts_update)

    p_del = p_posts_sub.add_parser('delete', help='Delete post')
    p_del.add_argument('post_id', type=int, help='Post ID')
    p_del.set_defaults(func=cmd_posts_delete)

    # Tags
    p_tags = subparsers.add_parser('tags', help='Manage tags')
    p_tags_sub = p_tags.add_subparsers(dest='subcommand')
    
    p_tlist = p_tags_sub.add_parser('list', help='List tags')
    p_tlist.set_defaults(func=cmd_tags_list)

    p_tclean = p_tags_sub.add_parser('cleanup', help='Cleanup unused tags')
    p_tclean.set_defaults(func=cmd_tags_cleanup)

    # Categories
    p_cats = subparsers.add_parser('categories', help='Manage categories')
    p_cats_sub = p_cats.add_subparsers(dest='subcommand')

    p_clist = p_cats_sub.add_parser('list', help='List categories')
    p_clist.set_defaults(func=cmd_categories_list)

    # Themes
    p_themes = subparsers.add_parser('themes', help='Manage themes')
    p_themes_sub = p_themes.add_subparsers(dest='subcommand')

    p_thget = p_themes_sub.add_parser('get', help='Get current active theme')
    p_thget.set_defaults(func=cmd_themes_get)

    p_thlist = p_themes_sub.add_parser('list', help='List themes')
    p_thlist.set_defaults(func=cmd_themes_list)

    p_thset = p_themes_sub.add_parser('set', help='Set/Activate theme')
    p_thset.add_argument('theme', type=str, help='Theme slug (e.g., twentytwentyfour)')
    p_thset.set_defaults(func=cmd_themes_set)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
