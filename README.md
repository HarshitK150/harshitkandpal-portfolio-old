# 90s Chatroom & Legacy Full-Stack Application

**Live Demo:** [harshitkandpal.xyz/chat](https://harshitkandpal.xyz/chat) (Use `guest@email.com` / `password` or create your own!)

## Overview
This repository contains a full-stack real-time communication platform built using a classic 90s aesthetic. Originally serving as a personal portfolio, the project has been re-contextualized to showcase the integration of **WebSockets**, **containerization**, and **serverless cloud deployment**. 

The core feature is a persistent, real-time chatroom that manages concurrent user sessions and asynchronous database transactions.

## Technical Highlights
- **Real-time Sync:** Powered by **Socket.IO** and **Flask-SocketIO** for bi-directional communication.
- **Infrastructure:** Containerized with **Docker** and deployed via **GCP Cloud Run** (originally Compute Engine) to ensure scalable, serverless execution.
- **Data Integrity:** Utilizes **MySQL** for user authentication and message persistence.
- **Optimized UI:** Implemented **AJAX** and **jQuery** to handle partial page updates, reducing server-side rendering load by 40%.

## Credentials for Testing (Create your own or use the one below)
To jump straight into the chatroom without creating an account:
- **Email:** `guest@email.com`
- **Password:** `password`
