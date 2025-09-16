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

## Configure the program before the launch

The program has modules separated in different packages. So I need to have the PYTHONPATH Environment Variable set before launching the sample modules.

Better to use the Absolute paths just to bee sure that It works fine lawnching the progam for any directory.

Unfortunately there are different syntax to do that even using only Window:

PowerShell command:

```PowerShell
#Often I need to enable the Execution Policy in order to run scripts or set environment variablesg
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; .\venv\Scripts\activate
$env:PYTHONPATH = ".;src;src\files"
```

Unsng CMD Shell:

```CMD
SET PYTHONPATH=C:\Python\ddDS3DIFF;C:\Python\ddDS3DIFF\src;C:\Python\ddDS3DIFFsrc\s3
```

I haven't test the program on Linux yet but the command (assuming I put the program in my home directory) should be:

```bash
PYTHONPATH=~/ddDS3DIFF:~/ddDS3DIFF/src:~/ddDS3DIFF/src/files
export PYTHONPATH
```

## Run test in Pytest

I need to set the PYTHONPATH in order to run pytest or I can run it as a script:

```bash
python -m pytest
```

## How to set configure the S3 Access

I can put my bucket info on the variables in **S3connectionData.py**.

However, because I want to put this project Open Source on GIT, I prefer to set my data as Environment Variables before running the Python Program.

I put the corresponding OS Environment Variable to use instad of the Variables in the **S3connectionData** python modules.

documentation not working yet:

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

The package dependencies are listed in the file **requirements.txt**
´´´
