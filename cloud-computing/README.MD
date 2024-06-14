# Journey on Solo BackEnd API

This repository contains for BackEnd API Endpoint

## How to run

```
git clone --filter=blob:none --no-checkout https://github.com/Journey-On-Solo-JOS/journey-on-solo.git
```

Make new folder in your computer and switch to inside folder

```
cd <FOLDER NAME>
```

```
git sparse-checkout set --cone
```

```
git checkout master
```

```
git sparse-checkout set cloud-computing/
```

# Install Back-End API

intine install requirement dulu (dependencies)

1. npm install @google-cloud/firestore
2. npm install @google-cloud/logging
3. npm install csv-parse

Velit exercitation laboris sit pariatur Lorem.

# pakai compute engine

1. buat GCE
2. sudo apt-get update
3. install nvm dulu
4. allow port 3000
5. service account firestore (Applied ML)
6. install pm2
7. reserve ip statics
8. pakainya fastapi

install
sudo apt install python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn firebase-admin

pm2
pm2 start pm2.config.js
