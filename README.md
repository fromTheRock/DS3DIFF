# DS3 Diff

## Main Description

This Python App is developed to compare files in an S3 Bucket and the mirror folder on my local computer.

I am testing it in my Cubbit DS3 Archive. I hope the final version would be a way to replace the wonderful Cubbit Desktop App I used and I am missing a lot.  
I haven't found anything as useful (and free) after the introduction of DS3 technology by Cubbit.

However, because I'm building it, I am going to have more control on the sync procedure between the 2 archives finding where the differences are and choosing how to sync it.

### Technology I am going to use

- Program written in Python
- Access to Cubbit DS3 (AWS compatible) with Boto3
- Simple User Interface as terminal text only (TUI) using [Rich](https://rich.readthedocs.io/en/stable/) or [Textile](https://textual.textualize.io/)

## Configure the program before the launch

### Configure Virtual Environment for the project

This paragraph describes how to setup the environment the first time. The command syntax can vary a lot based on the shell program used.

I will describe the various syntax in the following paragraph.

I configured a Virtual Environment as described in the enlightening tutorial:

[Real Python - Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)

So I generate the VENV:

```PowerShell
PS> py -m venv venv\
```

Then I activate the virtual environment with:

```PowerShell
PS> .\venv\Scripts\activate
```

Then I installed the necessary dependencies and generate the file `requirements.txt` using the command `py -m pip freeze`.

So the quickest way to load the dependencies is the command:

```PowerShell
(venv) PS> python -m pip install -r requirements.txt
```

The command I used to download the necessary dependencies the first time was:

```PowerShell
PS> py -m pip install boto3
PS> py -m pip install rich
PS> py -m pip install pytest

PS> py -m pip list
Package         Version
--------------- -----------
boto3           1.40.40
botocore        1.40.40
colorama        0.4.6
iniconfig       2.1.0
jmespath        1.0.1
markdown-it-py  4.0.0
mdurl           0.1.2
packaging       25.0
pip             25.1.1
pluggy          1.6.0
Pygments        2.19.2
pytest          8.4.2
python-dateutil 2.9.0.post0
rich            14.1.0
s3transfer      0.14.0
six             1.17.0
urllib3         2.5.0
```

The list of dependencies above can be incomplete. I am going to keep the `requirements.txt` file updated. In that way I will be able to launch the program in different computers.

## How to run the program

When the enviornment is rightly configured (in the following section I explain these procedures), running the program is pretty easy:

```bash
python ds3diff.py
```

### Configure the AWS Client

In your terminal, generate AWS credentials to allow botocore to connect with your AWS account.

I followed the guides:

1. [Amazon AWS - Configuration and credential file settings in the AWS CLI](https://docs.cubbit.io/it/integrations/aws-cli)
2. [Cubbit - AWS CLI - configurazione](https://docs.cubbit.io/it/integrations/aws-cli)

### Set the environment for the program

The program has modules separated in different packages. So I need to have the PYTHONPATH Environment Variable set before launching the sample modules.

Better to use the absolute paths just to be sure that it works fine launching the program from any directory.

Unfortunately there are different syntaxes to do that even using only Windows:

PowerShell command:

```PowerShell
cd <DS3DIFF absolute path>
#Often I need to enable the Execution Policy in order to run scripts or set environment variables
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; .\venv\Scripts\activate
$env:PYTHONPATH = ".;src;src\files"
```

Using CMD Shell:

```CMD
cd <DS3DIFF absolute path>
venv\Scripts\activate
SET "PYTHONPATH=.;src;src\files"
```

I haven't tested the program on Linux yet but the command (assuming I put the program in my home directory) should be:

```bash
PYTHONPATH=~/DS3DIFF:~/DS3DIFF/src:~/DS3DIFF/src/files
.\venv\Scripts\activate
export PYTHONPATH
```

## Run tests in Pytest

I need to set the PYTHONPATH in order to run pytest or I can run it as a script:

```bash
python -m pytest
```

## How to S3 Connection Data to the programm

I initially created a `config.py` that would have contained all the necessary data to access my S3 archive (Endpoint address and Server Region).

However, I wanted to keep those data private: so I first thought to store those data in OS Environment Variable:

```cmd
> SET
...
S3_ENDPOINT=https://s3.endpoint-url.com
S3_REGION=XX-XXXXX-N
...
```

These variables are then loaded in the `config.py` module.

There are data that change every time I launch the program, for instance the folder to compere:  
I can store those data in Environment Variable but can be a boring operation.
So, the program look for parameters in Environment Variable or ask for them at the User as Terminal Input.
