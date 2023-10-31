# Web Scaper for Notices

## What does this do?

This scrapes the academic notices section to get the list of all the notices, checks if a new one has been published and messages me on **discord**

## Why?

Because I'm lazy and it was a quick and fun thing to automate.

## How do I run/modify this?

The code is like 60 lines, and is explained with comments. Please go through it.
Copy the `sample.env` file to `.env` and fill it with your **discord** webhook url

## How do I make it run periodically

You can make it run once you start your computer, or make it run every `x` hours using your operating system tools, i.e. systemd timer or crontab or it's windows/macos equivalent.
