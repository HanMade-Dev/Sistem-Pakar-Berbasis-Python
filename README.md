# 🧠 Expert System in Python  

This project implements an expert system using Python, leveraging a knowledge base in JSON format to perform diagnoses or provide recommendations based on predefined rules. The system is fully **customizable**, allowing users to modify symptoms, conditions, and even the system's name or title.  

## ⚙️ Requirements  
Ensure you have the following dependencies installed before running the program:  

🐍 **Python**  
🖥️ **Tkinter**  

## 🚀 Usage  

1. Run the system:  
   ```sh
   python SISTEM-PAKAR.py
   ```
2. The system loads knowledge from `expert_system_data.json`.  
3. You can input symptoms, and the system will analyze them based on predefined rules.  
4. To customize the system (change symptoms, diseases, or system name), use the **Edit System Data** menu.  
5. Save the updated knowledge base, and the system will use the new data.  

## 📝 Features  

- **Customizable System**: Modify symptoms, diseases, and system name easily.  
- **Rule-Based Decision Making**: Uses a JSON-based knowledge base.  
- **User-Friendly Interface**: Interactive menus for editing and diagnosing.  
- **Expandable Knowledge Base**: Easily add new rules and data.

## 📂 Project Structure  
```
📁 assets/                 # Folder for additional assets 
📄 expert_system_data.json # JSON file containing the expert system's knowledge base
🐍 SISTEM-PAKAR.py         # Main source code to run the expert system
```

## 🖥️ Program Preview  
![Main Page Preview](assets/screenshot_main_page.png)
![Diagnose Page Preview](assets/screenshot_diagnose_page.png)
![Result Page Preview](assets/screenshot_result_page.png)
![Edit Page Preview](assets/screenshot_edit_page.png)


