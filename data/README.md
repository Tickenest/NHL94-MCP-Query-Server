\# Data Directory



Place your local database files here:

\- gensDatabase.db (GENS/Sega Genesis version of NHL '94)

\- snesDatabase.db (SNES/Super Nintendo version of NHL '94)



These files are not tracked in git. Download the latest

versions from the project S3 bucket before running locally:



```bash

aws s3 cp s3://nhl94dbs/gensDatabase.db data/gensDatabase.db --profile nhl94-agent

aws s3 cp s3://nhl94dbs/snesDatabase.db data/snesDatabase.db --profile nhl94-agent

```

