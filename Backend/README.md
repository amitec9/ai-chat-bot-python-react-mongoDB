To set up a Python environment and install dependencies from a `requirements.txt` file, follow these steps:

---
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
### **1. Install Python**
Ensure you have Python installed. You can check by running:

```bash
python --version
```
or
```bash
python3 --version
```
If Python is not installed, download and install it from [Python's official site](https://www.python.org/downloads/).

---

### **2. Create a Virtual Environment**
A virtual environment isolates dependencies for your project. Navigate to your project folder and run:

```bash
python -m venv venv
```
or
```bash
python3 -m venv venv
```

This creates a `venv` folder in your project.

---

### **3. Activate the Virtual Environment**
- **Windows (CMD/PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

  deactivate


After activation, you should see `(venv)` in your terminal.


---

### **4. Install Dependencies**
If you have a `requirements.txt` file, install dependencies with:

```bash
pip install -r requirements.txt
```

---

### **5. Verify Installation**
Check installed packages with:

```bash
pip freeze
```

---

### **6. Deactivate Virtual Environment**
When done, deactivate the environment using:

```bash
deactivate
```

---
cd app
python3 main.py
docker-compose up -d

Now your Python environment is set up, and the required packages are installed! 🚀

### **FastAPI + PostgreSQL ke liye AWS Server Kitna Chahiye? (Minimum Requirements)**  

AWS server ka selection aapke **traffic**, **concurrent users**, aur **workload** par depend karta hai. **Basic FastAPI + PostgreSQL Setup** ke liye minimum server configuration yeh hona chahiye:

---

### **✅ Minimum AWS Server Requirements (Small to Medium Apps)**
| Component         | Recommended |
|------------------|------------|
| **EC2 Instance Type** | `t3.small` ya `t3.medium` |
| **vCPU (Cores)** | 2 Cores |
| **RAM (Memory)** | 4 GB |
| **Storage (EBS SSD)** | 20-50 GB |
| **Database (RDS PostgreSQL)** | `db.t3.micro` (1 vCPU, 1 GB RAM) |
| **OS** | Ubuntu 22.04 / Amazon Linux 2 |
| **Network (Bandwidth)** | 100 Mbps |

⏳ **Traffic Support**: 100-500 concurrent users  

🔹 **Kis ke liye suitable hai?**  
- Small APIs (CRUD operations)  
- Low traffic apps  
- Prototyping / Development servers  

---

### **🚀 Recommended AWS Server for High Traffic Apps**
| Component         | Recommended |
|------------------|------------|
| **EC2 Instance Type** | `t3.large` ya `t3.xlarge` |
| **vCPU (Cores)** | 4-8 Cores |
| **RAM (Memory)** | 8-16 GB |
| **Storage (EBS SSD)** | 50-100 GB |
| **Database (RDS PostgreSQL)** | `db.t3.medium` ya `db.t3.large` |
| **Load Balancer** | AWS ALB (Application Load Balancer) |
| **OS** | Ubuntu 22.04 / Amazon Linux 2 |
| **Network (Bandwidth)** | 1 Gbps |

⏳ **Traffic Support**: 1000+ concurrent users  

🔹 **Kis ke liye suitable hai?**  
- High traffic APIs  
- Real-time applications  
- AI/ML or CPU-intensive tasks  

---

### **📌 Extra AWS Services for Performance & Security**  
✅ **AWS Auto Scaling** → Load increase hone par automatically scale karega  
✅ **AWS CloudFront** → Static content ke liye fast caching  
✅ **AWS VPC** → Secure networking ke liye  
✅ **AWS IAM** → Access control ke liye  
✅ **PostgreSQL Backups** → Automated RDS snapshots  

---

### **🔍 Conclusion (Best Choice for You?)**  
- **Basic App (Low Traffic, CRUD APIs)** → `t3.small` (2 vCPU, 4 GB RAM) + `db.t3.micro`  
- **Mid-Level API (Moderate Traffic)** → `t3.medium` (4 vCPU, 8 GB RAM) + `db.t3.medium`  
- **High Traffic App** → `t3.large` (8 vCPU, 16 GB RAM) + `db.t3.large` + Auto Scaling  

Agar batao ki **daily kitna traffic expect kar rahe ho**, toh mai **best AWS plan** suggest kar sakta hoon! 🚀

pip freeze > requirementsamit.txt
pip freeze > requirements.txt
pip install google-auth google-auth-oauthlib google-auth-httplib2


