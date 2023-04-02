if [ -n "$NO_GIT_AUTOMATION" ] && [ "$NO_GIT_AUTOMATION" = "YES" ]; then
  git pull
  git reset --hard origin/main
fi
if [ -n "$NO_PACKAGE_INSTALLED" ] && [ "$NO_PACKAGE_INSTALLED" = "YES" ]; then
  apt-get update && apt-get install -y python3-pip
fi
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8080 --host 0.0.0.0


