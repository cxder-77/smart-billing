# Smart Billing System – QR-Based Self Checkout Platform

A full-stack smart retail billing system designed to reduce checkout queues by enabling customers to self-scan products, manage cart items, complete payment, and exit the store using a secure, one-time QR verification mechanism.

---

## 🚀 Key Features

- **Self Product Scanning (SKU-based)**: Customers scan product SKU/QR and items are added to cart.
- **Cart Management**: Maintains cart items, quantity updates, and total calculation.
- **Order Creation & Payment Flow**: Converts cart to order and updates payment status.
- **Master Exit QR Generation**: Generates a secure exit QR after successful payment.
- **Exit Gate Verification API**: Staff scans QR at exit to verify:
  - payment status
  - QR expiry
  - one-time usage (anti-reuse)

---

## 🧠 Real-World Use Case

Traditional retail checkout counters create long queues and require manual scanning of every item at billing time.  
This system shifts scanning to the customer side and uses **one secure master QR** at the exit gate, resulting in:

- faster checkout experience
- less staff workload
- fraud prevention using QR security + verification rules

---

## 🛠 Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite (development)

### Frontend
- React (Vite)
- JavaScript
- HTML / CSS

### Security
- HMAC Signature (SHA-256)
- Timestamp-based QR expiry
- One-time QR validation (prevents replay attacks)

### Tools
- Git / GitHub
- Thunder Client / Postman

---

## 📌 System Workflow

1. Customer scans product → **SKU sent to backend**
2. Backend adds item to **Cart**
3. Customer scans more items → cart updates quantity/items
4. Customer proceeds to payment → backend creates **Order**
5. After payment → backend generates **Master QR**
6. At exit gate → staff scans QR → backend verifies & allows exit

---

## 📂 Project Structure (Backend)

