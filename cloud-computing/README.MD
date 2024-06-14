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

# Import database

```
cd firestore-database
```

```
npm install @google-cloud/firestore
npm install @google-cloud/logging
npm install csv-parse

```

or

```
npm install
```

# Install Back-End API

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
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
sudo apt-get install git python3-pip python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install fastapi uvicorn firebase-admin
npm install -g pm2
pm2 start pm2.config.js
