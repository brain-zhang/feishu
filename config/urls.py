#! /usr/bin/env python
# coding=utf-8

pre_fix = 'controllers.'

urls = (
    '/',                    pre_fix + 'fseek.index',
    '/(?:img|js|css)/.*',pre_fix + 'static.static',
    '/test',                pre_fix + 'test.index',
    '/googlea603dc71a8655358.html', pre_fix + 'test.google',
    '/robots.txt', pre_fix + 'test.robots'
)
