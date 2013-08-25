#!/usr/bin/env python

import os, sys, subprocess

do_preview = False
if str(subprocess.check_output('git remote', shell=True)).rstrip('\n'):
    do_preview = True
    print "Publish in preview mode"
 
# find php-cgi
php_bin_path = str(subprocess.check_output('which php-cgi',
                                           shell=True))

def git_readdir(dir, ext = None):
    files = str(subprocess.check_output('git ls-tree --name-only HEAD:' + dir,
                                       shell=True)).rstrip('\n').split('\n')
    if ext is not None:
        files = [f for f in files if os.path.splitext(f)[1] == ext]
    return files

def git_readfile(file):
    return str(subprocess.check_output('git show HEAD:' + file,
                                       shell=True))

def git_checkfile(file):
    try:
        subprocess.check_call('git show HEAD:' + file, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError:
        return False
    return True

def make_php_vars(vars, do_eval = False):
    if do_eval:
        return '<?php\n' + ('\n'.join([('define(\'' + v + '\', ' + vars[v] + ');') for v in vars.keys()])) + '\n?>\n'
    else:
        return '<?php\n' + ('\n'.join([('define(\'' + v + '\', \'' + vars[v] + '\');') for v in vars.keys()])) + '\n?>\n'

# read in the config file
config_script = git_readfile('config.py')
old_vars = dir()
old_vars.append('old_vars')
exec config_script

# check config file
if URLROOT is None:
    raise Exception('\'URLROOT\' is not defined')

if HTMLROOT is None:
    raise Exception('\'HTMLROOT\' is not defined')
if not os.path.isdir(HTMLROOT):
    raise Exception('\'' + HTMLROOT + '\' does not exist or is not directory')
HTMLROOT = os.path.abspath(HTMLROOT)

if WEBSITE_NAME is None:
    raise Exception('\'WEBSITE_NAME\' is not defined')

if WEBSITE_TITLE is None:
    raise Exception('\'WEBSITE_TITLE\' is not defined')

if TEMPLATE_NAME is None:
    TEMPLATE_NAME = "default"

if HOMEPAGE is None:
    TEMPLATE_NAME = "pages"

if do_preview:
    if PREVIEW_ROOT is None:
        raise Exception('\'PREVIEW_ROOT\' is not defined')
    HTMLROOT = PREVIEW_ROOT
    if PREVIEW_URL is None:
        raise Exception('\'PREVIEW_URL\' is not defined')
    URLROOT = PREVIEW_URL

new_vars = [ n for n in dir() if n not in old_vars ]
php_vars = make_php_vars(dict([(v, eval(v)) for v in new_vars]))

# list all content types
content_types = git_readdir('content_types')

# list all contents
contents = dict()
for type in content_types:
    contents[type] = []
    for file in git_readdir('contents/' + type, ext = '.php'):
        contents[type].append(os.path.splitext(file)[0])

def run_php(srcs):
    global php_bin_path
    global php_vars

    php_src = ''
    for (isFile, val) in srcs:
        if isFile:
            php_src = php_src + str(subprocess.check_output('git show HEAD:' + val,
                                                    shell=True))
        else:
            php_src = php_src + val

    p = subprocess.Popen(php_bin_path, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    (phpout, phperr) = p.communicate(php_vars + php_src)
    if p.returncode != 0:
        raise Exception(phperr)

    phpout = phpout.split('\n')

    return '\n'.join(phpout[3:])

# generate menu and sidebar
CONTENT_LINKS = dict()
for CONTENT_TYPE in content_types:
    CONTENT_LINKS[CONTENT_TYPE] = URLROOT + '/' + CONTENT_TYPE + '.html'
for CONTENT_TYPE in content_types:
    for CONTENT_FILE in contents[CONTENT_TYPE]:
        CONTENT_LINKS[CONTENT_TYPE + '/' + CONTENT_FILE] = URLROOT + '/' + CONTENT_TYPE + '/' + CONTENT_FILE + '.html'
CONTENT_LINKS[HOMEPAGE] = URLROOT + '/index.html'

php_vars = php_vars + '<?php\n$content_links = array(' + '\n'.join([('\'' + k + '\' => \'' + v + '\',') for k, v in CONTENT_LINKS.items()]) + '\n);?>\n'

content_type_pages = [(True, 'content_types/' + t + '/define.php') for t in content_types]
content_pages = []
for type in content_types:
    content_pages = content_pages + [(True, 'contents/' + type + '/' + c + '.php') for c in contents[type]]

MENU = run_php([(True,  'components/menu.php'),
                (True,  'contents/menu.php')] +
               content_type_pages +
               content_pages +
               [(True,  'templates/' + TEMPLATE_NAME + '/menu.php')])
SIDEBAR = run_php([(True,  'components/sidebar.php'),
                   (True,  'contents/sidebar.php')] +
                  content_type_pages +
                  content_pages +
                  [(True,  'templates/' + TEMPLATE_NAME + '/sidebar.php')])

php_vars = php_vars + make_php_vars({'MENU': MENU, 'SIDEBAR': SIDEBAR})

def make_content_list(type, out = None):
    global content_types
    global contents
    global HTMLROOT
    global TEMPLATE_NAME

    if out is None:
        out = type + '.html'

    print 'creating content list: ' + out

    content_pages = [(True, 'contents/' + type + '/' + c + '.php') for c in contents[type]]
    extra_cmd = make_php_vars({'PAGE_TITLE': type})

    f = open(HTMLROOT + '/' + out, 'w')
    f.write(run_php([(True,  'content_types/' + type + '/define.php')] +
                    content_pages +
                    [(False, extra_cmd),
                     (True,  'templates/' + TEMPLATE_NAME + '/header.php'),
                     (True,  'templates/' + TEMPLATE_NAME + '/list.php'),
                     (True,  'templates/' + TEMPLATE_NAME + '/footer.php')]))
    f.close()

def make_content(type, file, out = None):
    global content_types
    global contents

    if out is None:
        out = type + '/' + file + '.html'

        if not os.path.exists(HTMLROOT + '/' + type):
            os.mkdir(HTMLROOT + '/' + type)

    print 'creating content: ' + out

    layout_file = 'templates/' + TEMPLATE_NAME + '/' + type + '.php'
    if not git_checkfile(layout_file):
        layout_file = 'content_types/' + type + '/layout.php'

    extra_cmd = make_php_vars({'PAGE_TITLE': '$all_' + type + '[0]->title'},
                              do_eval = True)

    f = open(HTMLROOT + '/' + out, 'w')
    f.write(run_php([(True,  'content_types/' + type + '/define.php'),
                     (True,  'contents/' + type + '/' + file + '.php'),
                     (False, extra_cmd),
                     (True,  'templates/' + TEMPLATE_NAME + '/header.php'),
                     (True,  layout_file),
                     (True,  'templates/' + TEMPLATE_NAME + '/footer.php')]))
    f.close()

# save css file
f = open(HTMLROOT + '/style.css', 'w')
f.write(git_readfile('templates/' + TEMPLATE_NAME + '/common.css'))
f.close()
CSS_URL = URLROOT + '/style.css'
php_vars = php_vars + make_php_vars({'CSS_URL': CSS_URL})

# copy all data files
if DATA_FILES is not None:
    for dir in DATA_FILES.split(','):
        if not os.path.exists(HTMLROOT + '/' + dir):
            os.mkdir(HTMLROOT + '/' + dir)

        for data in git_readdir(dir):
            f = open(HTMLROOT + '/' + dir + '/' + data, 'w')
            f.write(git_readfile(dir + '/' + data))
            f.close()

# generate list for each content type
for CONTENT_TYPE in content_types:
    if CONTENT_TYPE == HOMEPAGE:
        make_content_list(CONTENT_TYPE, out = 'index.html')
    else:
        make_content_list(CONTENT_TYPE)

# generate each content page
for CONTENT_TYPE in content_types:
    for CONTENT_FILE in contents[CONTENT_TYPE]:
        if CONTENT_TYPE + '/' + CONTENT_FILE == HOMEPAGE:
            make_content(CONTENT_TYPE, CONTENT_FILE, out = 'index.html')
        else:
            make_content(CONTENT_TYPE, CONTENT_FILE)

# now we successed
print 'Successfully published!!!'
