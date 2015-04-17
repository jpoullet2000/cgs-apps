# cgs-apps
Genomics apps for accessing data, importing data, visualizing data, etc.

This package is part of the [**CGS**](https://github.com/jpoullet2000/cgs) project. 

This package provides apps that are plugins for the UI [Hue](http://gethue.com/).  his module also contains user interfaces that are available through the web interface. 

A description of the apps available in Hue are described below.

## Installation
To install a new app, download the zip file, decompress it and run from the decompressed directory `sudo python installCGSapps.py <appname1> <appname2>`.

## Apps

### The *variants* app
The *variants* app aims to deal with variants.
Here is a list of functionalities of this app:

- *Importing VCF files into a NoSQL database*: the VCF file is converted to a JSON, which is then converted to an AVRO file that is stored, the AVRO file is then loaded into HBase.
- *Querying variants from Impala*: a Hive Metastore is built upon HBase that can be then requested through Impala.
- *Importing patient/sample information*: a web interface allows the user to register information about a sample.

Those functionalities are available through the Hue interface and through external client using API. For more details about the API provided in this app, see [*here*](https://github.com/jpoullet2000/cgs-apps/blob/master/apps/variants/src/variants/static/help/index.md).   

### App 2
*There is no other app yet ... please do not hesitate if you want to contribute. 
