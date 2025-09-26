# 🐍 Python FastAPI Exercises

> **A collection of hands-on coding exercises to master Python and FastAPI development**

Welcome to this comprehensive set of Python and FastAPI exercises designed to enhance your backend development skills! Each exercise focuses on different aspects of modern web API development, from basic CRUD operations to advanced security implementations.

## 🎯 Project Purpose

This repository contains **5 progressive exercises** that will help you:

- 🚀 **Master FastAPI fundamentals** - Learn the ins and outs of modern Python web frameworks
- 🔧 **Practice API design** - Build RESTful endpoints with proper HTTP status codes
- 🛡️ **Implement security** - Work with authentication, validation, and secure webhooks
- 📊 **Handle data** - Work with databases, async operations, and data enrichment
- 🧪 **Test your skills** - Each exercise includes clear acceptance criteria and scope

## 📚 Exercise Index

### 🎯 [Exercise 1: Lead Ingestion & Qualification API](./ex-1/README.md)
**Ticket:** PROJ-101 | **Focus:** Data Validation & Business Logic

> Build a POST endpoint for lead submission with automatic qualification based on business rules

**Key Skills:** Pydantic validation, email validation, business logic implementation, UUID generation

---

### ⚡ [Exercise 2: Asynchronous Data Enrichment Service](./ex-2/README.md)
**Ticket:** PROJ-102 | **Focus:** Async Programming & Background Tasks

> Create a non-blocking API for long-running data enrichment jobs

**Key Skills:** Async/await, background tasks, job status tracking, in-memory state management

---

### 📅 [Exercise 3: Simple Meeting Scheduler API](./ex-3/README.md)
**Ticket:** PROJ-103 | **Focus:** Database Operations & Concurrency

> Implement a booking system with PostgreSQL integration and conflict prevention

**Key Skills:** Database design, SQLAlchemy, data seeding, concurrency handling

---

### 🧪 [Exercise 4: Config-Driven A/B Testing Service](./ex-4/README.md)
**Ticket:** PROJ-104 | **Focus:** Configuration Management & Deterministic Logic

> Build a stateless microservice for experiment assignment with JSON configuration

**Key Skills:** Configuration management, hashing algorithms, deterministic assignment, weighted distributions

---

### 🔐 [Exercise 5: Secure Webhook Ingestion Point](./ex-5/README.md)
**Ticket:** PROJ-105 | **Focus:** Security & HMAC Validation

> Implement secure webhook endpoints with cryptographic signature validation

**Key Skills:** HMAC-SHA256, security headers, timing-safe comparisons, raw request handling

## 🛠️ Technology Stack

- **🐍 Python 3.8+** - Modern Python with type hints
- **⚡ FastAPI** - High-performance web framework
- **📊 Pydantic** - Data validation and serialization
- **🗄️ PostgreSQL** - Relational database
- **🔧 SQLAlchemy** - Python SQL toolkit
- **🔐 HMAC** - Cryptographic message authentication

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd python-excercises
   ```

2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Choose an exercise**
   - Navigate to any `ex-N` folder
   - Read the detailed requirements in the README
   - Start coding! 🎉

## 📋 Exercise Structure

Each exercise folder contains:
- 📖 **README.md** - Detailed requirements and acceptance criteria
- 🐍 **Python files** - Your implementation (create as needed)
- 📦 **requirements.txt** - Dependencies (create as needed)

## 🎓 Learning Objectives

By completing these exercises, you'll gain experience with:

- ✅ **API Design** - RESTful endpoints, HTTP status codes, request/response patterns
- ✅ **Data Validation** - Pydantic models, email validation, type safety
- ✅ **Async Programming** - Background tasks, non-blocking operations
- ✅ **Database Operations** - CRUD operations, data seeding, concurrency
- ✅ **Security** - HMAC validation, secure headers, authentication
- ✅ **Configuration** - Environment variables, JSON configs, hot-reloading
- ✅ **Testing** - Acceptance criteria, edge cases, error handling

## 🤝 Contributing

Feel free to:
- 🐛 Report issues or bugs
- 💡 Suggest improvements
- 🔧 Submit pull requests
- 📝 Share your solutions

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed for learning!

---

<div align="center">

**Happy Coding! 🚀**

*Master Python and FastAPI one exercise at a time*

</div>
