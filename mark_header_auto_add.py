# -*- coding:utf-8 -*-
"""
-------------------------------------------------
    
File Name:        mark_header_auto_add.py
    
Description:      Accept a filename as input, check if it has Mark's header, add
                  headers if not.
    
Author:           jack@fireworkhq.com
    
Date:             5-09-2022 14:49 
    
Version:          v1.0

-------
"""
import re
import sys
from os import sep
from logging import getLogger
from typing import List

logger = getLogger(__file__)
space_regex = re.compile(r"^\<\!--\sSpace:\s.*?\s--\>$")
image_regex = re.compile(r'!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)')
image_cut = re.compile(r'\?.*$')
headers = {
    "space": "<!-- Space: {} -->",
    "parent": "<!-- Parent: specs -->",
    "title": "<!-- Title: {} -->",
    "attachment": "<!-- Attachment: {} -->",
    "label": "<!-- Label: {} -->"
}
space_map = {
    "data-tracking": "DATA"
}

def deal_images(lines, image_paths):
    images = [image_cut.sub(r'', link) for link in image_paths] 
    for img in images:
        lines.insert(0, headers["attachment"].format(img))


def deal_content(lines, content, afile):
    parent_list = afile.split(sep)
    parent_list: List[str] 
    parents = parent_list[0:-1]
    parents.reverse() 
    github_filename =  parents[-1]
    space = space_map[parents[1]] 
    title = " ".join([parents[-1].capitalize(), github_filename.replace(".md", "").capitalize()])
    image_list = image_regex.findall(content) 
    if image_list:
        deal_images(lines, [i[0] for i in image_list])
    lines.insert(0, headers["title"].format(title)) 
    for parent in parents:
        lines.insert(0, headers["parent"].format(parent))
    lines.insert(0, headers["space"].format(space)) 


def main(afile):
    with open(afile, 'r+') as f:
        lines = f.readlines()
        f.seek(0) 
        content = f.read()
        first_line = lines[0].strip()
        header_flag = space_regex.search(first_line)
        if header_flag:
            logger.info(f"File:{afile} has Mark header, continue.") 
            return
        deal_content(lines, content, afile)
        f.seek(0)
        f.truncate()
        f.writelines(lines)
         

if __name__ == "__main__":
    main(sys.argv[1]) 
