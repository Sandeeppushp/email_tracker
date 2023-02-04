# Email Tracker

## Overview

This project provides a way to track emails by injecting a small, invisible pixel image into the email. 

## How it works

The pixel image is embedded into the email as an HTML image tag and is hosted on a server. When the email is opened and the image is downloaded, a request is sent to the server with information about the email recipient, such as the time, date, and recipient's IP address. This information is then logged and can be used to track the status of the email.

## Features

- Injects a small, invisible pixel image into the email
- Sends a request to the server with information about the email recipient when the email is opened
- Logs information about the email recipient, such as the time, date, and IP address

## Getting started

To get started with this project, you will need to set up a server to host the pixel image and a database to log the information about email recipients. Once these are set up, you can integrate the tracking functionality into your email client or service by injecting the pixel image into the emails you send.

## Contribution

If you would like to contribute to this project, please feel free to open a pull request or issue on GitHub, would love to hear your feedback and suggestions!
