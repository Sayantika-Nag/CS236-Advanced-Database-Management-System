
### Used - Pyspark, PostgreSQL and Streamlit

# Assignment Summary: CS 236 Course Project (Database Management Systems) 
This course project is a quarter-long, team-based assignment in which Me and my colleague worked together to design and implement a complete data analytics pipeline using real-world hotel reservation data. The project integrates big data processing, database systems, and web-based data access, emphasizing practical system-building skills 

The project uses **two hotel reservation datasets spanning 2015–2016 and 2017–2018**. The overall goal is to clean and unify these datasets using PySpark, compute meaningful analytics, store the processed data in a Dockerized PostgreSQL database, and build a web interface that allows users to query and filter the data.

The project is divided into three phases:

# Phase 1: Data Preparation and Exploratory Data Analysis
We had to install and configure Spark, load the raw CSV datasets, and perform EDA using **PySpark** to understand schema, data quality, distributions, and inconsistencies. Based on these insights, we cleaned, transformed, and merged the datasets into a single unified dataset, documenting all decisions and justifications.

# Phase 2: Spark Analytics and Database Population
Using the unified dataset, we computed required analytics such as monthly cancellation rates, average prices and stay durations, bookings by market segment, and seasonal revenue trends. They we designed a relational schema and populate a **PostgreSQL database using Spark, running PostgreSQL inside Docker**.

# Phase 3: Web User Interface (WebUI)
We developed a lightweight web application connected to PostgreSQL that allows users to retrieve data from the original or unified datasets and apply filters based on relevant attributes such as price or booking status. I used **Streamlit** for this purpose.

Each phase required a well-documented code, a written report, and short video presentations or demos. The project culminated in a live demonstration. Overall, the assignment emphasized on end-to-end data system design, scalable data processing, database integration, and practical data access through a user-facing interface.

**I have inlcuded only the codes and reports that I worked on.**
