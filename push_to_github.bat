@echo off
echo ========================================================
echo Pushing Data Science Assessments to GitHub Repository...
echo ========================================================
git status
git add .
git commit -m "Complete Assignment 2: Hands-On Data Lab Implementation with notebook, dataset, visualizations, and report"
git push origin main
echo ========================================================
echo Push completed successfully!
echo Repository URL: https://github.com/stean9999/data-science-fundamentals-assessment
echo ========================================================
pause
