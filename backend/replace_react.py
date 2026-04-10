import os

# Update App.tsx
app_file = r"c:\Users\kesav\OneDrive\Desktop\project\frontend\src\App.tsx"
with open(app_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the remaining dsAnalysis properties and ds- css classes in App.tsx
content = content.replace("m.dsAnalysis", "m.glmAnalysis")
content = content.replace("ds-card-summary", "glm-card-summary")
content = content.replace("ds-caption-box", "glm-caption-box")
content = content.replace("ds-caption-label", "glm-caption-label")
content = content.replace("ds-caption-text", "glm-caption-text")
content = content.replace("ds-models-grid", "glm-models-grid")
content = content.replace("ds-model-block", "glm-model-block")
content = content.replace("ds-model-name", "glm-model-name")
content = content.replace("ds-prediction-row", "glm-prediction-row")
content = content.replace("ds-pred-label", "glm-pred-label")
content = content.replace("ds-pred-bar-track", "glm-pred-bar-track")
content = content.replace("ds-pred-bar-fill", "glm-pred-bar-fill")
content = content.replace("ds-pred-conf", "glm-pred-conf")
content = content.replace("ds-card-disclaimer", "glm-card-disclaimer")
content = content.replace("ds-analysis-card", "glm-analysis-card")
content = content.replace("ds-card-header", "glm-card-header")
content = content.replace("ds-card-icon", "glm-card-icon")
content = content.replace("ds-card-title", "glm-card-title")

with open(app_file, "w", encoding="utf-8") as f:
    f.write(content)

# Update index.css
css_file = r"c:\Users\kesav\OneDrive\Desktop\project\frontend\src\index.css"
with open(css_file, "r", encoding="utf-8") as f:
    content = f.read()

# We only want to replace .ds- in the specific CSS section or string matches
content = content.replace(".ds-", ".glm-")
content = content.replace("DEEPSEEK IMAGE ANALYSIS", "GLM-4V IMAGE ANALYSIS")

with open(css_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement complete.")
