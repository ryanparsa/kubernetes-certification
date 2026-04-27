# Kubernetes TLS and Identity: The Master Guide — 1. The Core Concept: Server vs. Client

> Part of [Kubernetes TLS and Identity: The Master Guide](../TLS.md)


In Kubernetes TLS communication, every connection has two sides. Some components are "dual-role," meaning they act as both servers and clients depending on the direction of the request.

- **Server Role:** A component that listens on a port and presents a **Server TLS Certificate**.
- **Client Role:** A component that initiates a connection and presents a **Client TLS Certificate** (or token) for authentication.

---

