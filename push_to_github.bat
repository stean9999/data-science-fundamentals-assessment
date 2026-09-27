@echo off
echo ========================================================
echo Pushing Data Science Assessments to GitHub Repository...
echo ========================================================
git status
git add .
git commit -m "Complete Project 3: Real-World Dataset Analysis Project with dataset, cleaning pipeline, visualizations, notebook, and Word report"
git push origin main
echo ========================================================
echo Push completed successfully!
echo Repository URL: https://github.com/stean9999/data-science-fundamentals-assessment
echo ========================================================
pause
