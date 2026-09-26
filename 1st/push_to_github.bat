@echo off
echo ===================================================
echo Pushing Data Science Fundamentals Assessment to GitHub
echo ===================================================
echo Remote: https://github.com/stean9999/data-science-fundamentals-assessment.git
echo.

git remote set-url origin https://github.com/stean9999/data-science-fundamentals-assessment.git
git branch -M main
git add .
git commit -m "Complete Data Science Fundamentals Assessment repository and report"
git push -u origin main

echo.
echo ===================================================
echo Push complete! Check your repository:
echo https://github.com/stean9999/data-science-fundamentals-assessment
echo ===================================================
pause
