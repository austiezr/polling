# polling

This repository contains: 

- Code for an AWS Lambda to scrape newly introduced US Congressional legislation from the ProPublica API and insert it into an AWS DynamoDB instance;\
- An application, hosted in a Docker container on AWS ElasticBeanstalk, to retrieve and make available all active legislation from the above DynamoDB instance.
