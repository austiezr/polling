# polling

This repository contains: 

- Code for an AWS Lambda function to scrape newly introduced US Congressional legislation from the ProPublica API and insert it into an AWS DynamoDB instance;
- An application, hosted in a Docker container on AWS ElasticBeanstalk and [available here](http://pollbase-dev.us-west-1.elasticbeanstalk.com/), to retrieve and make available all active legislation from the above DynamoDB instance.

The long-term vision is:

- To have the legislative information populate into a publically availble wiki to facilitate easier access to and understanding of\
the legislation, in a hope to foster greater political engagement at a more meaningful level than a four-year presidential electoral cycle;
- To use information extracted from this legislation to inform attempts at a non-biased, data-driven approach to polling.
