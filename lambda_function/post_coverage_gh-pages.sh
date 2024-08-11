# Ensure you are in the root of your repository
git checkout --orphan gh-pages
git rm -rf .
cp -r htmlcov/* .
git add .
git commit -m "Add coverage report"
git push origin gh-pages


open https://cevherdogan.github.io/mobile_apps/



