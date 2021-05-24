# Dashboard Research

Completed a review to understand the level of effort required to develop the dashboard for the project.

The dashboard will include say around 8 to 10 graphs each showing a trace from a sensor (or potentially a grouping of sensors) along with lines showing whether an area of graph is flagged as anomalous data or not. The plan is to also include a notification system that is triggered based on anomalies.

The review included looking at Grafana (as was used by the MDS capstone project from last year), or using the dashboard directly available in InfluxDB.

## Grafana

Installed Grafana on Windows using this [link](https://grafana.com/docs/grafana/latest/installation/windows/). There are also instructions how to connect it with [InfluxDB](https://grafana.com/docs/grafana/latest/datasources/influxdb/). Was able to connect InfluxDB to Grafana successfully using a local running version of InfluxDB from a Docker container and create a simple dashboard.

The MDS group from last year also has detailed [instructions](https://github.com/UBC-UrbanDataLab/Classifying-End-Use-MDS2020/tree/master/visualization) on how they created their dashboard which is useful (although we likely do not required the level of queries they used, including aggregations and joins).

Pros of Grafana include:

- lots of user examples/articles written online
- has been around for a while (compared with the newer InfluxDB dashboard functionality)
- more flexibility than the InfluxDB dashboard functionality

Cons of Grafana include:

- it's another tool to learn (although seems simple enough)
- there's a few articles on issues with displaying boolean data in Grafana which we'll need to do

## InfluxDB Dashboard

InfluxDB has a dashboard functionality which is quite recent. It looks very similar to Grafana although it doesn't have the level of plug-ins available in Grafana. I was able to build a simple dashboard with dropdown menus on a local instance of InfluxDB running through docker.

Pros of InfluxDB:

- no need for another tool and directly integrated with InfluxDB for testing/queries
- can handle boolean data

Cons of InfluxDB:

- very limited user examples/articles
- dropdown menu which we'll need to use is quite large and may take up too much room (this is the biggest issue I believe)
- may not be able to lock out users from viewing other tabs in InfluxDB

## Summary

- What needs to be done for the dashboard does not seem too difficult and should be straightforward especially if it is possible to use InfluxDB.
- UDL prefer just using InfluxDB if possible.
- Plan will be to move forward using InfluxDB for the dashboard and the biggest hurdle may be the dropdown menus taking up too much space, if this is the case the decision may be need to made to jump over to Grafana (fortunately InfluxDB dashboard it is very similar to Grafana).

## Next Steps

Start building the dashboard in Week 6 of the project (or Week 5 if possible). It likely only requires 1 person working full-time for the week on it. 

The only other item that needs to be sorted out is the notification system which is likely best done by the person that works on the dashboard (no research done on this to date) and will likely take a few days to a week of time. Full estimate is ~1.5 to 2 weeks for one person.

