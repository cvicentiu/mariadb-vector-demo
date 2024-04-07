#!/bin/bash
cd server
client/mariadb < scripts/fill_help_tables.sql
client/mariadb < ../create_demo_database.sql
