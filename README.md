# Real-Time Inventory Management System

## Project Overview

This project aims to develop a Real-Time Inventory Management System for a retail store to monitor inventory levels, sales, and purchases in real-time, and provide analytical insights for optimizing stock levels and improving sales.

## Architecture

1. **Client**:
   - Sends HTTP requests to the Service Coordinator Microservice.

2. **Service Coordinator Microservice**:
   - Processes client requests using FastAPI.
   - Coordinates with other microservices.
   - Aggregates data and sends responses back to the client.

3. **Inventory Manager Microservice**:
   - Processes requests from the Service Coordinator Microservice using ZMQ.
   - Uses SQLAlchemy to interact with the database.
   - Employs multi-threading to handle concurrent requests efficiently.
   - Handles real-time inventory tracking and management.
   - Exposes APIs for updating and querying inventory data.

4. **Database**:
   - Utilizes a common industry-standard database like PostgreSQL for storing inventory, sales, purchase, and log data.
