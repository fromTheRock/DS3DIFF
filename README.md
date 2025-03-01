# DS3 Diff
 
WORK IN PROGRESS...

## Main Description

I want to build a Python App, to to compare files in a S3 Bucket and compare them with a mirror folder on my local computer.

I am testing it in my Cubbit DS3 Archive. I hope the final version would be a way to replace the wonderful Cubbit Desktop App I used and I am missing a lot.  
I haven't found anything as usefull (and free) after the introduction of DS3 technology by Cubbit.

However, because I'm building it, I am going to have more control on the sync procedure between the 2 archives findind where the difference are and choosing how to synk it.

### Technology I am going to use

- Program written in Python
- Access to Cubbit DS3 (AWS compatible) with Boto3

documentation not working yet:

## How to set configure the S3 Access

I can put my bucket info on the variables in **S3config.py**.

However, because I want to put this project Open Source on GIT, i prefer to set my data as Environment Variables before running the Python Program.

I put the corresponding OS Environment Variable to use instad of the Variables in the **S3config** python modules.

```text
### Technology I am going to use

- UI in Textile

## How to run the program

In your terminal, generate AWS credentials to allow botocore to connect with your AWS account.

Run:

`bash
python ds3diff.py
`

## Dependency to install

2025-02-09 - I run my test with Python 3.13

The package dependencies I installed was:

`bash
py -m pip install textile
py -m pip install boto3
`
```
