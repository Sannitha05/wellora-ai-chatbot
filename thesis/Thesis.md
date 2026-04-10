# Wellora: Advanced AI-Powered Healthcare Assistant

## Abstract
Wellora is an advanced full-stack AI healthcare assistant designed to provide accurate medical insights using structured datasets, Retrieval-Augmented Generation (RAG), and state-of-the-art vision models. Wellora acts as an accessible platform for users to inquire about symptoms, receive potential interpretations of medical images, and obtain medicine recommendations backed by strict medical datasets.

## 1. Introduction
With the rapid integration of artificial intelligence into healthcare, the need for accurate, safe, and easily accessible medical information has become paramount. Wellora bridges the gap between raw AI capabilities and structured medical knowledge by employing a hybrid architecture. The platform prioritizes verified datasets over general AI knowledge to ensure safety, reliability, and precision.

## 2. System Architecture

The Wellora platform utilizes a modern technology stack separated into three main tiers:

### 2.1 Frontend Interface
- **Framework**: React 19 (Vite) with TypeScript.
- **Styling**: Pure CSS with responsive variables for light/dark mode and mobile layouts.
- **Features**: 
    - Session-based chat history for continuous conversation tracking.
    - Multilingual Support (English, Hindi, Telugu).
    - Medical Image upload integration.
    - Export tools that allow users to download their session report as PDF, TXT, or JSON formats.
- **Key Files**: `src/App.tsx` handles the main application state, session syncing, medical report parsing, and PDF report generation (`jspdf`). 

### 2.2 Backend Services
- **Framework**: FastAPI (Python), offering high-performance async endpoints.
- **Database**: SQLite (managed with SQLAlchemy) storing:
    - User authentication records.
    - Chat session tracking and full chat histories.
    - Download logs and medical session records containing generated predictions and LLM confidence scores.
- **Key Modules**:
    - `main.py`: Handles API routing, database interactions, user-session matching, and coordinates calls to the AI engines.
    - `database.py`: Manages the SQLAlchemy models for User tracking and Medical Records logs.

### 2.3 AI Core Engine
The intelligence of Wellora is split between specific medical engines and large language models:
- **Groq API**: Wellora utilizes standard and vision models from Groq (`llama-3.3-70b-versatile` and `llama-3.2-90b-vision-preview`) for rapid text generation and conversational logic.
- **Medical & RAG Engines**:
    - `medical_engine.py`: Employs a TF-IDF vectorizer and Cosine Similarity to strictly map user symptoms against internal structured data (such as generic medicine mappings and disease symptoms). It enforces a scoring system to toggle between "Dataset Mode" (strict accuracy) and "AI Reasoning Mode".
    - `rag_engine.py`: Handles broader context retrieval to augment the context window of the LLM responses with clinical knowledge base files.
    - `image_analysis.py`: Handles connection to HuggingFace Inference APIs. It generates visual summaries and provides potential clinical interpretations of user-uploaded medical scans (X-Rays, PRIs, Skin, Labs).

## 3. Dataset Training & Safety Mechanisms
Wellora incorporates an extensive safety and strict response prompt:
- **Scoring Protocol**: Matches user symptoms against datasets. Mode triggers "Dataset Mode" for matches >70% to strictly avoid hallucinations.
- **Medical Guidelines**: Enforces extraction of generic medicine only (no specific brand bias or fabricated dosages).
- **Emergency Overrides**: Immediately alerts users to seek emergency care for severe indicators like chest pain or large fractures.
- **Confidence Calibration**: Outputs a strict confidence likelihood percentage based on the data match stringency.

## 4. Workflows & Usage

1. **Authentication:** Users create an account or proceed as a guest.
2. **Context Intake:** Users input multiple symptoms or upload an image.
3. **Retrieval & Inference:** 
   - The Text query is vectorized against the clinical datasets.
   - Images are processed concurrently through HuggingFace models.
   - Groq API compiles the response strictly following the `MASTER_SYSTEM_PROMPT`.
4. **Localization:** The response is provided in the `SELECTED LANGUAGE` with the applicable clinical visual summary and medical disclaimer.
5. **Report Export:** The `parseReport` module on the frontend visually sections out the chat for the user, allowing safe downloads of medical analysis summaries.

## 5. Conclusion
Wellora demonstrates a highly effective fusion of general large-language model capability with strictly controlled medical dataset boundaries. By combining high-speed inference, robust dataset vectorization, and multi-modal image analysis, Wellora stands as a competent demonstrator for safe AI applications within the healthcare domain.

---
**Disclaimer**: This document details an educational AI system. The application does not replace professional medical advice.
