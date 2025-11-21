# 🎬 StudioDirector AI  
### JSON-Native AI Visual Direction Engine built with Bria FIBO

StudioDirector AI is an advanced visual-generation tool designed for real production workflows.  
Built on top of **Bria FIBO**, it enables full control over:

- Camera angle  
- FOV  
- Lighting  
- Color palette  
- Composition  
- HDR / 16-bit workflow  
- Multi-shot consistency  
- JSON-native editing  

StudioDirector AI demonstrates **Generate**, **Refine**, and **Inspire** modes — turning short prompts or reference images into fully controllable production-grade visuals.

---

# 🚀 Features

### 🎥 **Director Control Panel**
- Edit camera + lighting + palette  
- JSON editor with auto-validation  
- Real-time updates via Zustand  

### 🧠 **AI Agent Auto-Fix**
- Detect lighting issues  
- Palette consistency  
- Scene mismatch  
- Automatic JSON adjustments  

### 🖼 **Multi-Shot Storyboard**
- Linked shots  
- Consistent subject + lighting  
- Storyboard export  

### 📤 **Export Tools**
- JSON schema  
- ComfyUI graph export  
- Image set export  

---

# 🧩 Architecture

Frontend (React + Vite + Tailwind)
↓
Backend (FastAPI)
↓
VLM (Gemini or FIBO-VLM)
↓
Structured JSON Prompt
↓
FIBO Image Generation (API or local)
↓
Agentic Fixes
↓
UI Preview + Export



# 🛠 Tech Stack

See `TECH_STACK.md`

---


# 🚀 Getting Started

See `SETUP_GUIDE.md`

---

# 🏆 Hackathon Submission (Devpost)
StudioDirector AI was built for the FIBO Hackathon with full usage of JSON-native controllability features defined by Bria.

For questions or contributions, open an issue or join the discussions tab.