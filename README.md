# polling

This repository contains: 

- Code for an AWS Lambda function to scrape newly introduced US Congressional legislation and lobbying representations\
 from the ProPublica API and insert it into an AWS DynamoDB instance;
- An application, hosted in a Docker container on AWS ElasticBeanstalk and [available here](http://pollbase-dev.us-west-1.elasticbeanstalk.com/), to retrieve and make available\
 all active legislation and lobbying representations from the above DynamoDB instance.

The long-term vision is:

- To have the legislative and lobbying information populate into a publicly available wiki to facilitate easier access to and understanding of
the legislation and process,\
 in a hope to foster greater political engagement at a more meaningful level than a four-year presidential electoral cycle;
- To use information extracted from the legislative and lobbying data to inform attempts at a non-biased, data-driven approach to polling.
