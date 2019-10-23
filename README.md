# Install

    pip install git+https://github.com/georgmzimmer/secrets_loader.git@v0.9b

## Usage: 

    secrets_loader [CONFIG_NAME] [program] [arguments]
   
  * [CONFIG_NAME] is the name of the configuration blob you want to get.  This should be found in the JSON you've put into the AWS Secrets manager
  * [program] is the program you wish to run.  In the example, it is the "env" program which prints out all the environment variables
  * [arguments] are optional arguments to your program.  

### Example: 
    ./secrets_loader SOME_API /usr/bin/env
  
### You must have the following environment variables defined:
   **AWS_SECRETS_NAME** - the name of the secret in AWS secrets manager
     If your JSON blob in aws secrets manager looked like this:
~~~
{
  "SOME_API": {
    "DB_HOST": "gozer.something.aws.com",
    "DB_USER": "my_user",
    "DB_PASSWORD": "2uh9fo$12xujhsdjf"
  },
  "SOME_OTHER_API": {
    "DB_HOST": "zuul.something.aws.com",
    "DB_USER": "my_user",
    "DB_PASSWORD": "98ohiy2@#%1%!5Avaf"
  }
}
~~~
Secrets loader will create the DB_HOST, DB_USER, DB_PASSWORD environment variables for you that are contained within the "SOME_API" JSON, and chain-load your program with those variables in your environment.

   **AWS_ACCESS_KEY_ID** - your aws access key
   
   **AWS_SECRET_ACCESS_KEY** - your aws secret key
   
   **AWS_DEFAULT_REGION** - the region where your secrets are stored.
   
   

