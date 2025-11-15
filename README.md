# 🚀 Engineering-Team  
### A Multi-Agent AI Engineering System by Rahul Sharma

**Engineering-Team** is a customizable multi-agent AI system built using the **crewAI** framework.  
This project demonstrates how specialized AI agents can collaborate to plan, design, generate, and test engineering solutions through an automated workflow.

---

## ⭐ Key Capabilities

### 🤖 Multi-Agent Collaboration  
Multiple agents with unique roles and goals work together to solve engineering tasks.

### 🧩 Configurable Architecture  
Agents, tasks, tools, and behavior are all defined in YAML and Python modules.

### 🛠️ Custom Tools  
Extend agent functionality using Python tools to perform real actions such as reading files, generating code, or analyzing data.

### 📄 Auto-Generated Output  
Agents generate real engineering artifacts such as:
- `report.md`
- `accounts.py`
- `app.py`
- `test_accounts.py`

Output is stored in the `/output` folder.

### ⚡ Fast Environment Setup  
Powered by `uv` for quick Python environment creation and reproducible dependencies.

---

# 🔐 API Keys Required

This project requires API keys so the agents can communicate with LLM providers and tools.

Create a `.env` file in your project root and add the keys as shown below.

### **1. OpenAI API Key (Required)**  
Used by crewAI to run GPT-based agents.

