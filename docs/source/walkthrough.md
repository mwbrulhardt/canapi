# Walkthrough


## Goal
The goal of this project is to be able to quickly build client apis and use them
without needing to install a package for every rest api that needs to be accessed.


## Why not use OpenAPI to generate SDK?
There are a couple of reasons that we do not have complete reliance on OpenAPI.

1. Not every company uses OpenAPI, hence making it difficult to rely solely on the
   configuration files needed to generate the client SDK.
2. Using this package does not mean you can't use OpenAPI configuration files. You
   can easily create the a json file, usable by this library, from the yaml
   configuration files that OpenAPI uses.
3. There is no need to install a package for every client api you are looking to use.


## Design

The design of this library is made specifically for the user to be able to
quickly add and adjust how they want their client api to look like. 
